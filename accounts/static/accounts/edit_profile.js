//Photo preview
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

//Bio character count
document.addEventListener("DOMContentLoaded", () => {
    const bio = document.querySelector("#id_bio");
    const counter = document.querySelector("#bio-counter");
    if (bio && counter) {
        const update = () => {
            counter.textContent = `${bio.value.length} / 300`;
        };
        bio.addEventListener("input", update);
        update();
    }
});

//Slider for age range
document.addEventListener("DOMContentLoaded", () => {
    const minAge = document.querySelector("#min-age");
    const maxAge = document.querySelector("#max-age");
    const display = document.querySelector("#age-display");
    const hiddenMin = document.querySelector("input[name='preferred_min_age']")
    const hiddenMax = document.querySelector("input[name='preferred_max_age']")
    if (minAge && maxAge && display && hiddenMin && hiddenMax) {
        const update = () => {
            let min = parseInt(minAge.value);
            let max = parseInt(maxAge.value);
            if (min > max) {
                [minAge.value, maxAge.value] = [max, min];
            }
            display.textContent = `${minAge.value} - ${maxAge.value}`;
            hiddenMin.value = minAge.value;
            hiddenMax.value = maxAge.value;
        };
        minAge.addEventListener("input", update);
        maxAge.addEventListener("input", update);
        update();
    }
})