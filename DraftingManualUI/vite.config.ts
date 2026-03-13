import { defineConfig } from 'vite';

export default defineConfig({
	// Only process the root index.html as an entry point.
	// HTML files in public/ are served as-is and should not be resolved as modules.
	appType: 'spa',
	// Base path for GitHub Pages deployment at /commonwealth-leg-drafting-manual/
	base: '/commonwealth-leg-drafting-manual/',
});
