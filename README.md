# cpp_wasm_notebook

A test repository to see If i could compile a C++ quarto notebook to wasm and run it as a website

## Documentation

To create a notebook like the one described here all you need is a qmd file which is being compiled that contains cpp and includes some html/js which runs the generated wasm file.
To start, just copy over the scripts file and make sure you use the in `_quarto.yml` you have the following line

```yml
project:
  pre-render: scripts/render_cpp.py
  resources: "*.wasm"
```

This ensures that the wasm is copied over to the final rendered project as well as compiles down the cpp codeblocks to wasm

From there look to the `cpp` directory to get an idea of how to structure a wasm notebook by the given DVD bounce example. Note that this is raw wasm from clang, so you have to interface with the javascript on your own, as well as remembering that there is no standard library, however if need be you can modify the script to link with [newlibc](https://github.com/bminor/newlib).
