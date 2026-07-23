document.addEventListener("click", function (e) {
  document.querySelectorAll(".score-dropdown").forEach(function (dd) {
    if (!dd.contains(e.target)) {
      dd.querySelector(".score-list").classList.add("hidden");
    }
  });
});

document.querySelectorAll(".score-btn").forEach(function (btn) {
  btn.addEventListener("click", function (e) {
    e.stopPropagation();
    const dropdown = btn.closest(".score-dropdown");
    const list = dropdown.querySelector(".score-list");
    document.querySelectorAll(".score-list").forEach(function (l) {
      if (l !== list) l.classList.add("hidden");
    });
    list.classList.toggle("hidden");
  });
});

document.querySelectorAll(".score-option").forEach(function (opt) {
  opt.addEventListener("click", function () {
    const dropdown = opt.closest(".score-dropdown");
    const value = opt.dataset.value;
    const label = value === "" ? "--" : value;
    dropdown.querySelector(".score-value").textContent = label;
    dropdown.querySelector("input[type=hidden]").value = value;
    dropdown.querySelectorAll(".score-option").forEach(function (o) {
      o.classList.remove("bg-primary-700");
    });
    if (value !== "") opt.classList.add("bg-primary-700");
    dropdown.querySelector(".score-list").classList.add("hidden");
  });
});

document.querySelectorAll(".pen-toggle").forEach(function (checkbox) {
  checkbox.addEventListener("change", function () {
    const id = checkbox.dataset.matchId;
    const fields = document.querySelector(`.pen-fields[data-match-id="${id}"]`);
    fields.classList.toggle("hidden", !checkbox.checked);
  });
});

document.getElementById("prediction-form").addEventListener("submit", function (e) {
  const homeInput = document.querySelector('input[name="home_ft"]');
  const awayInput = document.querySelector('input[name="away_ft"]');
  if (!homeInput.value || !awayInput.value) {
    e.preventDefault();
    alert("Оберіть рахунок для обох команд");
  }
});