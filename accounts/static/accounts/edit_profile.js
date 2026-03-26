//Photo Preview
document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.querySelector("#id_image");
    const preview = document.querySelector("#photo-preview");
    if (fileInput) {
        fileInput.addEventListener("change", (e) => {
            const file = e.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = (event) => {
                preview.innerHTML = `
                    <img src="${event.target.result}"
                        style="width:120px;height:120px;border-radius:8px;object-fit:cover;opacity:0.7;">
                `;
            };
            reader.readAsDataURL(file);
        });
    }
});