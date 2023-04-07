<script>
  let files;

  let source_code = "<pending>";
  let gpt_response = "<pending>";
  let evaluate_button;

  const uploadFile = async () => {
    console.log("uploading!");
    if (files.length != 1) {
      window.location.reload();
      return;
    }

    const file = files[0];
    file.text().then((text) => {
      source_code = text;
    });
    evaluate_button.classList.remove("secondary");
    evaluate_button.removeAttribute("disabled");
  };

  const sendToGPT = async () => {
    console.log("Asking GPT for suggestions...");
    console.log("sending code: ", source_code);
    evaluate_button.setAttribute("aria-busy", "true");
    evaluate_button.classList.add("secondary");
    const base_url = "http://127.0.0.1:8000/get_suggestion";
    const body = {
      loc: 1,
      language: "Python",
      source_code: source_code,
    };

    fetch(base_url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    })
      .then((resp) => resp.json())
      .then((data) => {
        gpt_response = data.message;
        evaluate_button.setAttribute("aria-busy", "false");
        evaluate_button.setAttribute("disabled", "true");
      });
  };
</script>

<main class="container">
  <h1>GPT Variables</h1>
  <article>
    <h2>Upload Code</h2>
    <label for="file"
      >File browser
      <input bind:files type="file" id="file" name="file" />
    </label>
    <button on:click={uploadFile}>Submit</button>
  </article>

  <article>
    <h3>Source Code</h3>
    <textarea readonly="true" bind:value={source_code} />
    <button on:click={sendToGPT} bind:this={evaluate_button}>Evaluate</button>
  </article>

  <article>
    <h3>GPT's Evaluation</h3>
    <textarea readonly="true" bind:value={gpt_response} />
  </article>
</main>

<style>
  textarea {
    min-height: 50vh;
  }
</style>
