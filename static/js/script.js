document
.getElementById("imageInput")
.addEventListener("change", (event) => {
  const input = event.target;
  const previewImage = document.getElementById("previewImage");
  const hiddenDiv = document.getElementById("hidden-div");
  const fileError = document.getElementById('fileError');
  if (input.files && input.files[0]) {
    const file = input.files[0];
    const fileType = file.type.split('/').pop().toLowerCase();
    if (fileType !== 'jpeg' && fileType !== 'png' && fileType !== 'jpg') {
      fileError.classList.remove('hidden');
      previewImage.src = ''; // Clear preview image if file format is incorrect
      input.value = '';
      hiddenDiv.classList.remove('display-box');
      hiddenDiv.classList.add('hidden');
      return;
    }

    fileError.classList.add('hidden');
    hiddenDiv.classList.remove('hidden');
  hiddenDiv.classList.add('display-box');
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.src = e.target.result;
    };
    reader.readAsDataURL(input.files[0]);
  }
});

function generateCaption() {
  const imageInput = document.getElementById("imageInput");
  const hiddenDiv = document.getElementById("hidden-div");
  const generatedCaption = document.getElementById("generated-caption");
  const outputDiv = document.getElementById('output')

  if (imageInput.files && imageInput.files[0]) {
    const formData = new FormData();
    formData.append("image", imageInput.files[0]);

    fetch("/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.text())
      .then((caption) => {
        // hiddenDiv.classList.add("display-box");
        outputDiv.classList.remove('hidden');
        outputDiv.style.display = 'flex';
        generatedCaption.textContent =  caption;
      })
      .catch((error) => console.error("Error:", error));
  } else {
    console.error("No image selected");
  }
}

function playSpeech() {
  const generatedCaption = document.getElementById("generated-caption");
  const text = generatedCaption.textContent.trim();
  if (text) {
    fetch("/play_speech", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: text }),
    })
      .then((response) => {
        if (response.ok) {
          console.log("Speech played successfully");
        } else {
          console.error("Failed to play speech");
        }
      })
      .catch((error) => console.error("Error:", error));
  }
}