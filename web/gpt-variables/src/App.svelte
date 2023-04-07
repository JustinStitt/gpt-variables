<script>
  import { fade } from "svelte/transition";

  let files;

  let source_code = "<pending>";
  let source_code_header, source_code_article, gpt_evaluation_article;
  let gpt_response = "<i>pending...</i>";
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
    source_code_article.removeAttribute("hidden");
    window.scrollTo(0, document.body.scrollHeight);
  };

  const sendToGPT = async () => {
    console.log("Asking GPT for suggestions...");
    console.log("sending code: ", source_code);
    evaluate_button.setAttribute("aria-busy", "true");
    evaluate_button.classList.add("secondary");
    const base_url = "https://gptvar.jstitt.dev/api/get_suggestion";
    const body = {
      loc: 1,
      language: "Python",
      source_code: source_code,
    };

    fetch(base_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
      body: JSON.stringify(body),
    })
      .then((resp) => resp.json())
      .then((data) => {
        gpt_response = data.message;
        evaluate_button.setAttribute("aria-busy", "false");
        evaluate_button.setAttribute("disabled", "true");
        gpt_evaluation_article.removeAttribute("hidden");
        gpt_evaluation_article.scrollIntoView();
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

  <article bind:this={source_code_article} hidden transition:fade>
    <h3 bind:this={source_code_header}>Source Code</h3>
    <textarea readonly bind:value={source_code} />
    <button on:click={sendToGPT} bind:this={evaluate_button}>Evaluate</button>
  </article>

  <article bind:this={gpt_evaluation_article} hidden>
    <h3>GPT's Evaluation</h3>
    <!-- <textarea readonly="true" bind:value={gpt_response} /> -->
    <p>{@html gpt_response}</p>
  </article>
</main>

<style>
  textarea {
    min-height: 50vh;
  }
</style>
