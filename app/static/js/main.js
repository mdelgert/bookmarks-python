/**
 * Live icon preview in the bookmark form.
 * Called from the icon_type <select> and icon_value <input> change handlers.
 */
function updateIconPreview(element) {
  const form = element.closest("form") || document.body;

  const typeEl  = form.querySelector('[name="icon_type"]');
  const valueEl = form.querySelector('[name="icon_value"]') || document.getElementById("icon_value_input");
  const preview = form.querySelector('#icon-preview') || document.getElementById("icon-preview");

  if (!typeEl || !valueEl || !preview) return;

  const type  = typeEl.value;
  const value = valueEl.value.trim();

  preview.innerHTML = "";

  if (!value) return;

  if (type === "mdi") {
    const i = document.createElement("i");
    i.className = `mdi mdi-${value}`;
    i.style.cssText = "font-size:1.4rem;color:#58a6ff;";
    preview.appendChild(i);

  } else if (type === "si") {
    const img = document.createElement("img");
    img.src   = `https://cdn.simpleicons.org/${encodeURIComponent(value)}/aaaaaa`;
    img.alt   = value;
    img.style.cssText = "width:24px;height:24px;object-fit:contain;";
    preview.appendChild(img);

  } else if (type === "selfhst") {
    const img = document.createElement("img");
    img.src   = `https://cdn.jsdelivr.net/gh/selfhst/icons/png/${encodeURIComponent(value)}.png`;
    img.alt   = value;
    img.style.cssText = "width:24px;height:24px;object-fit:contain;";
    img.onerror = () => { preview.innerHTML = '<i class="mdi mdi-image-off" style="color:#8b949e;"></i>'; };
    preview.appendChild(img);

  } else if (type === "url") {
    const img = document.createElement("img");
    img.src   = value;
    img.alt   = "icon";
    img.style.cssText = "width:24px;height:24px;object-fit:contain;";
    img.onerror = () => { preview.innerHTML = '<i class="mdi mdi-image-off" style="color:#8b949e;"></i>'; };
    preview.appendChild(img);
  }
}

// Initialize previews for any pre-filled edit forms already on the page
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('[name="icon_type"]').forEach(el => updateIconPreview(el));
});

// Re-initialize after HTMX swaps in new content (e.g. edit row)
document.addEventListener("htmx:afterSwap", () => {
  document.querySelectorAll('[name="icon_type"]').forEach(el => updateIconPreview(el));
});
