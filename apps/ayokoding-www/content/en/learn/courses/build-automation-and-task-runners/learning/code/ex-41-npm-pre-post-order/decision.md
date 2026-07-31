# npm prefix hook order

For a script named build, npm runs a matching prebuild script first, then build, then postbuild after a
successful build. No post-script runs when the main script fails.
