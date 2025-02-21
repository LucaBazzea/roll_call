
// this file is generated — do not edit it


/// <reference types="@sveltejs/kit" />

/**
 * Environment variables [loaded by Vite](https://vitejs.dev/guide/env-and-mode.html#env-files) from `.env` files and `process.env`. Like [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private), this module cannot be imported into client-side code. This module only includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) _and do_ start with [`config.kit.env.privatePrefix`](https://svelte.dev/docs/kit/configuration#env) (if configured).
 * 
 * _Unlike_ [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private), the values exported from this module are statically injected into your bundle at build time, enabling optimisations like dead code elimination.
 * 
 * ```ts
 * import { API_KEY } from '$env/static/private';
 * ```
 * 
 * Note that all environment variables referenced in your code should be declared (for example in an `.env` file), even if they don't have a value until the app is deployed:
 * 
 * ```
 * MY_FEATURE_FLAG=""
 * ```
 * 
 * You can override `.env` values from the command line like so:
 * 
 * ```bash
 * MY_FEATURE_FLAG="enabled" npm run dev
 * ```
 */
declare module '$env/static/private' {
	export const KDE_FULL_SESSION: string;
	export const PROFILEHOME: string;
	export const XDG_ACTIVATION_TOKEN: string;
	export const LANGUAGE: string;
	export const LC_TIME: string;
	export const USER: string;
	export const npm_config_user_agent: string;
	export const XDG_SEAT: string;
	export const XDG_SESSION_TYPE: string;
	export const npm_node_execpath: string;
	export const KONSOLE_VERSION: string;
	export const QT_WAYLAND_RECONNECT: string;
	export const SHLVL: string;
	export const npm_config_noproxy: string;
	export const HOME: string;
	export const KDE_APPLICATIONS_AS_SCOPE: string;
	export const OLDPWD: string;
	export const DESKTOP_SESSION: string;
	export const npm_package_json: string;
	export const GTK_RC_FILES: string;
	export const KDE_SESSION_VERSION: string;
	export const SHELL_SESSION_ID: string;
	export const XDG_SEAT_PATH: string;
	export const KONSOLE_DBUS_SESSION: string;
	export const LC_MONETARY: string;
	export const MANAGERPID: string;
	export const npm_config_userconfig: string;
	export const npm_config_local_prefix: string;
	export const DBUS_SESSION_BUS_ADDRESS: string;
	export const GSM_SKIP_SSH_AGENT_WORKAROUND: string;
	export const SSH_ASKPASS: string;
	export const SYSTEMD_EXEC_PID: string;
	export const P9K_TTY: string;
	export const npm_config_engine_strict: string;
	export const COLORTERM: string;
	export const KONSOLE_DBUS_WINDOW: string;
	export const COLOR: string;
	export const npm_config_metrics_registry: string;
	export const WAYLAND_DISPLAY: string;
	export const XKB_DEFAULT_LAYOUT: string;
	export const LOGNAME: string;
	export const JOURNAL_STREAM: string;
	export const QT_AUTO_SCREEN_SCALE_FACTOR: string;
	export const WINDOWID: string;
	export const _: string;
	export const npm_config_prefix: string;
	export const COLORFGBG: string;
	export const MEMORY_PRESSURE_WATCH: string;
	export const XDG_SESSION_CLASS: string;
	export const TERM: string;
	export const XDG_SESSION_ID: string;
	export const npm_config_cache: string;
	export const GTK2_RC_FILES: string;
	export const KGLOBALACCELD_PLATFORM: string;
	export const npm_config_node_gyp: string;
	export const PATH: string;
	export const INVOCATION_ID: string;
	export const SESSION_MANAGER: string;
	export const NODE: string;
	export const npm_package_name: string;
	export const LC_ADDRESS: string;
	export const XDG_MENU_PREFIX: string;
	export const XDG_RUNTIME_DIR: string;
	export const XDG_SESSION_PATH: string;
	export const XKB_DEFAULT_MODEL: string;
	export const DISPLAY: string;
	export const ICEAUTHORITY: string;
	export const LANG: string;
	export const LC_TELEPHONE: string;
	export const XDG_CURRENT_DESKTOP: string;
	export const XAUTHORITY: string;
	export const XDG_SESSION_DESKTOP: string;
	export const npm_lifecycle_script: string;
	export const SSH_AUTH_SOCK: string;
	export const LC_NAME: string;
	export const SHELL: string;
	export const npm_lifecycle_event: string;
	export const npm_package_version: string;
	export const QT_ACCESSIBILITY: string;
	export const KONSOLE_DBUS_SERVICE: string;
	export const LC_MEASUREMENT: string;
	export const LC_IDENTIFICATION: string;
	export const P9K_SSH: string;
	export const ANDROID_SDK_ROOT: string;
	export const XDG_VTNR: string;
	export const npm_config_globalconfig: string;
	export const npm_config_init_module: string;
	export const PWD: string;
	export const npm_config_globalignorefile: string;
	export const npm_execpath: string;
	export const XDG_CONFIG_DIRS: string;
	export const XDG_DATA_DIRS: string;
	export const _P9K_TTY: string;
	export const ANDROID_HOME: string;
	export const npm_config_global_prefix: string;
	export const LC_NUMERIC: string;
	export const QTWEBENGINE_DICTIONARIES_PATH: string;
	export const npm_command: string;
	export const KDE_SESSION_UID: string;
	export const LC_PAPER: string;
	export const MEMORY_PRESSURE_WRITE: string;
	export const INIT_CWD: string;
	export const EDITOR: string;
}

/**
 * Similar to [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private), except that it only includes environment variables that begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) (which defaults to `PUBLIC_`), and can therefore safely be exposed to client-side code.
 * 
 * Values are replaced statically at build time.
 * 
 * ```ts
 * import { PUBLIC_BASE_URL } from '$env/static/public';
 * ```
 */
declare module '$env/static/public' {
	
}

/**
 * This module provides access to runtime environment variables, as defined by the platform you're running on. For example if you're using [`adapter-node`](https://github.com/sveltejs/kit/tree/main/packages/adapter-node) (or running [`vite preview`](https://svelte.dev/docs/kit/cli)), this is equivalent to `process.env`. This module only includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) _and do_ start with [`config.kit.env.privatePrefix`](https://svelte.dev/docs/kit/configuration#env) (if configured).
 * 
 * This module cannot be imported into client-side code.
 * 
 * Dynamic environment variables cannot be used during prerendering.
 * 
 * ```ts
 * import { env } from '$env/dynamic/private';
 * console.log(env.DEPLOYMENT_SPECIFIC_VARIABLE);
 * ```
 * 
 * > In `dev`, `$env/dynamic` always includes environment variables from `.env`. In `prod`, this behavior will depend on your adapter.
 */
declare module '$env/dynamic/private' {
	export const env: {
		KDE_FULL_SESSION: string;
		PROFILEHOME: string;
		XDG_ACTIVATION_TOKEN: string;
		LANGUAGE: string;
		LC_TIME: string;
		USER: string;
		npm_config_user_agent: string;
		XDG_SEAT: string;
		XDG_SESSION_TYPE: string;
		npm_node_execpath: string;
		KONSOLE_VERSION: string;
		QT_WAYLAND_RECONNECT: string;
		SHLVL: string;
		npm_config_noproxy: string;
		HOME: string;
		KDE_APPLICATIONS_AS_SCOPE: string;
		OLDPWD: string;
		DESKTOP_SESSION: string;
		npm_package_json: string;
		GTK_RC_FILES: string;
		KDE_SESSION_VERSION: string;
		SHELL_SESSION_ID: string;
		XDG_SEAT_PATH: string;
		KONSOLE_DBUS_SESSION: string;
		LC_MONETARY: string;
		MANAGERPID: string;
		npm_config_userconfig: string;
		npm_config_local_prefix: string;
		DBUS_SESSION_BUS_ADDRESS: string;
		GSM_SKIP_SSH_AGENT_WORKAROUND: string;
		SSH_ASKPASS: string;
		SYSTEMD_EXEC_PID: string;
		P9K_TTY: string;
		npm_config_engine_strict: string;
		COLORTERM: string;
		KONSOLE_DBUS_WINDOW: string;
		COLOR: string;
		npm_config_metrics_registry: string;
		WAYLAND_DISPLAY: string;
		XKB_DEFAULT_LAYOUT: string;
		LOGNAME: string;
		JOURNAL_STREAM: string;
		QT_AUTO_SCREEN_SCALE_FACTOR: string;
		WINDOWID: string;
		_: string;
		npm_config_prefix: string;
		COLORFGBG: string;
		MEMORY_PRESSURE_WATCH: string;
		XDG_SESSION_CLASS: string;
		TERM: string;
		XDG_SESSION_ID: string;
		npm_config_cache: string;
		GTK2_RC_FILES: string;
		KGLOBALACCELD_PLATFORM: string;
		npm_config_node_gyp: string;
		PATH: string;
		INVOCATION_ID: string;
		SESSION_MANAGER: string;
		NODE: string;
		npm_package_name: string;
		LC_ADDRESS: string;
		XDG_MENU_PREFIX: string;
		XDG_RUNTIME_DIR: string;
		XDG_SESSION_PATH: string;
		XKB_DEFAULT_MODEL: string;
		DISPLAY: string;
		ICEAUTHORITY: string;
		LANG: string;
		LC_TELEPHONE: string;
		XDG_CURRENT_DESKTOP: string;
		XAUTHORITY: string;
		XDG_SESSION_DESKTOP: string;
		npm_lifecycle_script: string;
		SSH_AUTH_SOCK: string;
		LC_NAME: string;
		SHELL: string;
		npm_lifecycle_event: string;
		npm_package_version: string;
		QT_ACCESSIBILITY: string;
		KONSOLE_DBUS_SERVICE: string;
		LC_MEASUREMENT: string;
		LC_IDENTIFICATION: string;
		P9K_SSH: string;
		ANDROID_SDK_ROOT: string;
		XDG_VTNR: string;
		npm_config_globalconfig: string;
		npm_config_init_module: string;
		PWD: string;
		npm_config_globalignorefile: string;
		npm_execpath: string;
		XDG_CONFIG_DIRS: string;
		XDG_DATA_DIRS: string;
		_P9K_TTY: string;
		ANDROID_HOME: string;
		npm_config_global_prefix: string;
		LC_NUMERIC: string;
		QTWEBENGINE_DICTIONARIES_PATH: string;
		npm_command: string;
		KDE_SESSION_UID: string;
		LC_PAPER: string;
		MEMORY_PRESSURE_WRITE: string;
		INIT_CWD: string;
		EDITOR: string;
		[key: `PUBLIC_${string}`]: undefined;
		[key: `${string}`]: string | undefined;
	}
}

/**
 * Similar to [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private), but only includes variables that begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) (which defaults to `PUBLIC_`), and can therefore safely be exposed to client-side code.
 * 
 * Note that public dynamic environment variables must all be sent from the server to the client, causing larger network requests — when possible, use `$env/static/public` instead.
 * 
 * Dynamic environment variables cannot be used during prerendering.
 * 
 * ```ts
 * import { env } from '$env/dynamic/public';
 * console.log(env.PUBLIC_DEPLOYMENT_SPECIFIC_VARIABLE);
 * ```
 */
declare module '$env/dynamic/public' {
	export const env: {
		[key: `PUBLIC_${string}`]: string | undefined;
	}
}
