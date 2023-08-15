//const copyButtonLabel = "Copy Code";
const copyButtonLabel = '<i class="fa-solid fa-clipboard"></i>';

// use a class selector if available
let blocks = document.querySelectorAll("td.code > div > pre, div.highlight > pre");

blocks.forEach((block) => {
  // only add button if browser supports Clipboard API
  if (navigator.clipboard) {
    let button = document.createElement("button");

    button.innerHTML = copyButtonLabel;
    block.appendChild(button);

    button.addEventListener("click", async () => {
      await copyCode(block);
    });
  }
});

async function copyCode(block) {
  let code = block.querySelector("code");
  let text = code.innerText;

  await navigator.clipboard.writeText(text);
}
