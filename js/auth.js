(() => {
  const config = window.COGNITO_CONFIG || {};
  const storageKeys = {
    accessToken: "cognito_access_token",
    expiresAt: "cognito_access_token_expires_at",
    state: "cognito_oauth_state",
    verifier: "cognito_pkce_verifier"
  };

  function isConfigured() {
    return Boolean(config.domain && config.clientId && config.redirectUri);
  }

  function addGate(message, errorMessage = "") {
    let gate = document.getElementById("auth-gate");
    if (!gate) {
      gate = document.createElement("section");
      gate.id = "auth-gate";
      gate.setAttribute("aria-labelledby", "auth-title");
      document.body.appendChild(gate);
    }

    gate.innerHTML = `
      <div class="auth-card">
        <span class="brand-badge" style="margin-left: 0;">Amazon Cognito</span>
        <h1 id="auth-title">Sign in to your meeting workspace</h1>
        <p>${message}</p>
        ${errorMessage ? '<p class="auth-error" role="alert">' + escapeHtml(errorMessage) + '</p>' : ""}
        ${isConfigured() ? '<button type="button" class="btn btn-primary" id="cognito-sign-in">Continue with Cognito</button>' : ""}
      </div>`;

    const signIn = document.getElementById("cognito-sign-in");
    if (signIn) signIn.addEventListener("click", beginSignIn);
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, char => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
    })[char]);
  }

  function base64Url(bytes) {
    let binary = "";
    bytes.forEach(byte => { binary += String.fromCharCode(byte); });
    return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }

  async function sha256(value) {
    return new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value)));
  }

  function clearOAuthState() {
    sessionStorage.removeItem(storageKeys.state);
    sessionStorage.removeItem(storageKeys.verifier);
  }

  function getAccessToken() {
    const token = sessionStorage.getItem(storageKeys.accessToken);
    const expiresAt = Number(sessionStorage.getItem(storageKeys.expiresAt));
    if (!token || !Number.isFinite(expiresAt) || expiresAt <= Date.now() + 30000) {
      sessionStorage.removeItem(storageKeys.accessToken);
      sessionStorage.removeItem(storageKeys.expiresAt);
      return null;
    }
    return token;
  }

  async function beginSignIn() {
    if (!isConfigured()) return;
    if (!window.crypto || !crypto.subtle) {
      addGate("Sign-in requires HTTPS or localhost so the browser can create a secure PKCE challenge.");
      return;
    }

    const random = new Uint8Array(32);
    crypto.getRandomValues(random);
    const state = base64Url(random);
    const verifier = base64Url(crypto.getRandomValues(new Uint8Array(32)));
    sessionStorage.setItem(storageKeys.state, state);
    sessionStorage.setItem(storageKeys.verifier, verifier);

    const challenge = base64Url(await sha256(verifier));
    const url = new URL("/oauth2/authorize", config.domain);
    url.search = new URLSearchParams({
      client_id: config.clientId,
      response_type: "code",
      scope: "openid email profile",
      redirect_uri: config.redirectUri,
      state,
      code_challenge: challenge,
      code_challenge_method: "S256"
    }).toString();
    window.location.assign(url.toString());
  }

  async function completeSignIn() {
    const params = new URLSearchParams(window.location.search);
    const code = params.get("code");
    const returnedState = params.get("state");
    const oauthError = params.get("error_description") || params.get("error");
    if (oauthError) {
      clearOAuthState();
      addGate("Cognito could not complete sign-in.", oauthError);
      return false;
    }
    if (!code) return false;

    const expectedState = sessionStorage.getItem(storageKeys.state);
    const verifier = sessionStorage.getItem(storageKeys.verifier);
    clearOAuthState();
    if (!expectedState || returnedState !== expectedState || !verifier) {
      addGate("The sign-in response could not be verified. Please start again.", "The sign-in response is missing its valid state or PKCE verifier.");
      return false;
    }

    try {
      const response = await fetch(new URL("/oauth2/token", config.domain), {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          grant_type: "authorization_code",
          client_id: config.clientId,
          code,
          redirect_uri: config.redirectUri,
          code_verifier: verifier
        })
      });
      if (!response.ok) throw new Error(`Token exchange failed (${response.status}).`);
      const tokens = await response.json();
      if (!tokens.access_token || !Number.isFinite(Number(tokens.expires_in))) {
        throw new Error("Cognito returned an invalid token response.");
      }
      sessionStorage.setItem(storageKeys.accessToken, tokens.access_token);
      sessionStorage.setItem(storageKeys.expiresAt, String(Date.now() + Number(tokens.expires_in) * 1000));
      window.history.replaceState({}, document.title, window.location.pathname);
      return true;
    } catch (error) {
      addGate("Cognito sign-in failed. Check the app-client callback settings and try again.", error.message);
      console.error("Cognito token exchange failed:", error);
      return false;
    }
  }

  function signOut() {
    sessionStorage.removeItem(storageKeys.accessToken);
    sessionStorage.removeItem(storageKeys.expiresAt);
    if (!isConfigured()) {
      window.location.reload();
      return;
    }
    const url = new URL("/logout", config.domain);
    url.search = new URLSearchParams({
      client_id: config.clientId,
      logout_uri: config.redirectUri
    }).toString();
    window.location.assign(url.toString());
  }

  async function initialize() {
    const authButton = document.getElementById("auth-action");
    if (authButton) {
      authButton.addEventListener("click", () => {
        if (getAccessToken()) signOut();
        else beginSignIn();
      });
    }

    if (!isConfigured()) {
      addGate("Configure the Cognito domain, app client ID, and exact HTTPS callback URL in js/auth-config.js before using this app.");
      return;
    }

    if (new URLSearchParams(window.location.search).has("code") ||
        new URLSearchParams(window.location.search).has("error")) {
      if (!await completeSignIn()) return;
    }

    if (!getAccessToken()) {
      addGate("Sign in with your organization’s Amazon Cognito user pool to continue.");
      return;
    }

    if (authButton) {
      authButton.textContent = "Sign out";
      authButton.setAttribute("aria-label", "Sign out of Cognito");
    }
    document.body.classList.remove("auth-pending");
  }

  window.cognitoAuth = { getAccessToken };
  document.addEventListener("DOMContentLoaded", initialize, { once: true });
})();
