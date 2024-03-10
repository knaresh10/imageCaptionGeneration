document
.getElementById("imageInput")
.addEventListener("change", (event) => {
  const input = event.target;
  const previewImage = document.getElementById("previewImage");
  const hiddenDiv = document.getElementById("hidden-div");
  hiddenDiv.classList.remove('hidden');
  hiddenDiv.classList.add('display-box');
  if (input.files && input.files[0]) {
    console.log(input.files[0]);
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.src = e.target.result;
    };
    reader.readAsDataURL(input.files[0]);
  }
});