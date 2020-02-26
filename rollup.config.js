import svelte from "rollup-plugin-svelte";
import resolve from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import livereload from "rollup-plugin-livereload";
import { terser } from "rollup-plugin-terser";
import replace from "@rollup/plugin-replace";
import babel from "rollup-plugin-babel";

const production = !process.env.ROLLUP_WATCH;

export default {
  input: "src/front/main.js",
  output: {
    sourcemap: true,
    format: "iife",
    name: "app",
    file: "static/js/bundle.js"
  },
  plugins: [
    replace({ __production__: production ? "true" : "false" }),

    svelte({
      // enable run-time checks when not in production
      dev: !production,
      // we'll extract any component CSS out into
      // a separate file - better for performance
      css: css => {
        css.write("static/css/bundle.css");
      }
    }),

    // If you have external dependencies installed from
    // npm, you'll most likely need these plugins. In
    // some cases you'll need additional configuration -
    // consult the documentation for details:
    // https://github.com/rollup/plugins/tree/master/packages/commonjs
    resolve({
      browser: true,
      dedupe: ["svelte"]
    }),
    commonjs(),

    babel({
      extensions: [".js", ".mjs", ".svelte"],
      exclude: ["node_modules/core-js/**", "node_modules/whatwg-fetch/**"]
    }),

    // Watch the `public` directory and refresh the
    // browser on changes when not in production
    !production && livereload("static"),

    // If we're building for production (npm run build
    // instead of npm run dev), minify
    production && terser()
  ],
  watch: {
    clearScreen: false
  }
};
