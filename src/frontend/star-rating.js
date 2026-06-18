// Renders a 0-5 star rating with half-star support.
// In interactive mode, clicking the left/right half of a star sets a .5 or whole value.
function createStarRating(container, { initialRating = 0, interactive = false, onChange = () => {} } = {}) {
  let rating = initialRating;

  function render() {
    container.innerHTML = "";

    for (let i = 1; i <= 5; i++) {
      const wrap = document.createElement("span");
      wrap.className = "star-wrap";

      const bg = document.createElement("span");
      bg.className = "star-bg";
      bg.textContent = "★";

      const fillRatio = Math.max(0, Math.min(1, rating - (i - 1)));
      const fill = document.createElement("span");
      fill.className = "star-fill";
      fill.style.width = `${fillRatio * 100}%`;
      fill.textContent = "★";

      wrap.append(bg, fill);

      if (interactive) {
        const left = document.createElement("span");
        left.className = "star-click-zone left";
        left.addEventListener("click", () => {
          rating = i - 0.5;
          render();
          onChange(rating);
        });

        const right = document.createElement("span");
        right.className = "star-click-zone right";
        right.addEventListener("click", () => {
          rating = i;
          render();
          onChange(rating);
        });

        wrap.append(left, right);
      }

      container.append(wrap);
    }
  }

  render();

  return {
    get: () => rating,
    set: (value) => {
      rating = value;
      render();
    },
  };
}
