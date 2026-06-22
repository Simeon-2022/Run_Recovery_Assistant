"use strict";

// Works whether served from the FastAPI backend (localhost:8000)
// or opened directly as a local file (file://)
const API_BASE = (() => {
  const { origin, protocol } = window.location;
  if (protocol === "file:") {
    return "http://127.0.0.1:8000";
  }
  return origin;
})();

// ─── DOM refs ───────────────────────────────────────────────────

const form            = document.getElementById("recovery-form");
const durationInput   = document.getElementById("duration");
const mileageInput    = document.getElementById("mileage");
const paceInput       = document.getElementById("pace");
const intensityInput  = document.getElementById("intensity");
const intensityCurrent = document.getElementById("intensity-current");
const intensityDownBtn = document.getElementById("intensity-down");
const intensityUpBtn   = document.getElementById("intensity-up");
const intensitySteps   = Array.from(document.querySelectorAll(".intensity-step"));
const calorieTargetInput = document.getElementById("calorie-target");
const statusMessage   = document.getElementById("form-message");
const workoutBadge    = document.getElementById("workout-class");
const loadBadge       = document.getElementById("training-load");
const macroChart      = document.getElementById("macro-chart");
const macroLegend     = document.getElementById("macro-legend");
const resetBtn        = document.getElementById("reset-btn");

// Auto-calculate pace = duration / mileage
function recalcPace() {
  const duration = parseFloat(durationInput.value);
  const mileage  = parseFloat(mileageInput.value);
  if (duration > 0 && mileage > 0) {
    paceInput.value = (duration / mileage).toFixed(2);
  }
}

durationInput.addEventListener("input", recalcPace);
mileageInput.addEventListener("input", recalcPace);

const categoryLists = {
  carbs:         document.getElementById("carbs-list"),
  protein:       document.getElementById("protein-list"),
  antioxidants:  document.getElementById("antioxidants-list"),
  fats:          document.getElementById("fats-list"),
};

const MACRO_COLORS = {
  Carbs:   "#e6a844",
  Protein: "#3b7f9e",
  Fat:     "#9b7ec8",
};

const INTENSITY_LEVELS = [
  { value: "low", label: "Low" },
  { value: "moderate", label: "Moderate" },
  { value: "high", label: "High" },
  { value: "very_high", label: "Maximum" },
];

function getIntensityIndex(value) {
  const idx = INTENSITY_LEVELS.findIndex((x) => x.value === value);
  return idx >= 0 ? idx : 1;
}

let intensityIndex = getIntensityIndex(intensityInput?.value ?? "moderate");

function renderIntensityControl() {
  const level = INTENSITY_LEVELS[intensityIndex];
  if (intensityInput) intensityInput.value = level.value;
  if (intensityCurrent) intensityCurrent.textContent = level.label;

  intensitySteps.forEach((btn, idx) => {
    const active = idx === intensityIndex;
    btn.classList.toggle("is-active", active);
    btn.setAttribute("aria-pressed", active ? "true" : "false");
  });

  if (intensityDownBtn) intensityDownBtn.disabled = intensityIndex === 0;
  if (intensityUpBtn) intensityUpBtn.disabled = intensityIndex === INTENSITY_LEVELS.length - 1;
}

function setIntensity(nextIndex) {
  intensityIndex = Math.max(0, Math.min(INTENSITY_LEVELS.length - 1, nextIndex));
  renderIntensityControl();
}

if (intensityDownBtn && intensityUpBtn && intensitySteps.length) {
  intensityDownBtn.addEventListener("click", () => setIntensity(intensityIndex - 1));
  intensityUpBtn.addEventListener("click", () => setIntensity(intensityIndex + 1));
  intensitySteps.forEach((btn) => {
    btn.addEventListener("click", () => {
      const idx = Number.parseInt(btn.dataset.index ?? "1", 10);
      setIntensity(idx);
    });
  });
  renderIntensityControl();
}

// ─── Helpers ────────────────────────────────────────────────

function getPerceivedEffort() {
  const checked = document.querySelector('input[name="perceived_effort"]:checked');
  return checked ? Number.parseInt(checked.value, 10) : 3;
}

function setStatus(message, type = "info") {
  statusMessage.textContent = message;
  statusMessage.classList.remove("form-message--error", "form-message--success");

  if (type === "error") {
    statusMessage.classList.add("form-message--error");
  } else if (type === "success") {
    statusMessage.classList.add("form-message--success");
  }
}

function clearEl(el) {
  while (el.firstChild) el.removeChild(el.firstChild);
}

function createFoodCard(food, tone = "") {
  const li = document.createElement("li");
  if (tone) {
    li.dataset.tone = tone;
  }

  const name = document.createElement("strong");
  name.textContent = food.name;

  const meta = document.createElement("span");
  meta.className = "food-meta";
  meta.textContent = `${food.serving_size} · ${food.calories_per_serving ? `${food.calories_per_serving} kcal` : ""}${food.calories_per_100g ? ` (${food.calories_per_100g} kcal/100 g)` : ""}`;

  const desc = document.createElement("span");
  desc.className = "food-desc";
  desc.textContent = food.description;

  const nutrients = document.createElement("small");
  nutrients.textContent = `Nutrients: ${food.nutrients_summary}`;

  li.appendChild(name);
  li.appendChild(meta);
  li.appendChild(desc);
  li.appendChild(nutrients);
  return li;
}

function normalizeFoodKey(name) {
  return (name ?? "").trim().toLowerCase();
}

function buildFoodToneLookup(foodsByCategory) {
  const toneLookup = new Map();
  Object.entries(foodsByCategory ?? {}).forEach(([tone, foods]) => {
    (foods ?? []).forEach((food) => {
      const key = normalizeFoodKey(food?.name);
      if (key) {
        toneLookup.set(key, tone);
      }
    });
  });
  return toneLookup;
}

// ─── Donut Chart ────────────────────────────────────────────

function drawDonutChart(canvas, macros, options = {}) {
  const dpr = window.devicePixelRatio ?? 1;
  const cssSize = options.size ?? 180;
  const centerLabel = options.centerLabel ?? "Macros";
  const legendTarget = options.legendTarget ?? null;
  canvas.width  = cssSize * dpr;
  canvas.height = cssSize * dpr;
  canvas.style.width  = `${cssSize}px`;
  canvas.style.height = `${cssSize}px`;

  const ctx = canvas.getContext("2d");
  ctx.scale(dpr, dpr);

  const slices = [
    { label: "Carbs",   value: macros.carbs_percent,   color: MACRO_COLORS.Carbs },
    { label: "Protein", value: macros.protein_percent, color: MACRO_COLORS.Protein },
    { label: "Fat",     value: macros.fat_percent,     color: MACRO_COLORS.Fat },
  ];

  const total    = slices.reduce((s, d) => s + d.value, 0);
  const cx       = cssSize / 2;
  const cy       = cssSize / 2;
  const outerR   = cx - 8;
  const innerR   = outerR * 0.55;

  ctx.clearRect(0, 0, cssSize, cssSize);

  let startAngle = -Math.PI / 2;
  slices.forEach((slice) => {
    const angle = (slice.value / total) * 2 * Math.PI;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.arc(cx, cy, outerR, startAngle, startAngle + angle);
    ctx.closePath();
    ctx.fillStyle = slice.color;
    ctx.fill();
    startAngle += angle;
  });

  // Donut hole
  ctx.beginPath();
  ctx.arc(cx, cy, innerR, 0, 2 * Math.PI);
  ctx.fillStyle = "#ffffff";
  ctx.fill();

  // Centre label
  ctx.fillStyle = "#1f2623";
  ctx.font = "bold 10px 'Space Grotesk', sans-serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  if (centerLabel) {
    ctx.fillText(centerLabel, cx, cy);
  }

  if (legendTarget) {
    clearEl(legendTarget);
    slices.forEach((slice) => {
      const li  = document.createElement("li");
      const dot = document.createElement("span");
      dot.className = "legend-dot";
      dot.style.background = slice.color;
      const label = document.createElement("span");
      const kcalVal = slice.label === "Carbs"   ? macros.carbs_kcal
                    : slice.label === "Protein" ? macros.protein_kcal
                    : macros.fat_kcal;
      label.textContent = kcalVal
        ? `${slice.label}: ${slice.value}% · ${kcalVal} kcal`
        : `${slice.label}: ${slice.value}%`;
      li.appendChild(dot);
      li.appendChild(label);
      legendTarget.appendChild(li);
    });
  }
}

// ─── Render helpers ────────────────────────────────────────

function renderFoods(data) {
  Object.entries(categoryLists).forEach(([category, listEl]) => {
    clearEl(listEl);
    const foods = data.foods?.[category] ?? [];
    if (foods.length === 0) {
      const empty = document.createElement("li");
      empty.textContent = "No items found for this category.";
      listEl.appendChild(empty);
      return;
    }
    foods.forEach((food) => listEl.appendChild(createFoodCard(food)));
  });
}

function renderMealPlan(mealPlan, foodToneLookup) {
  mealPlan.forEach((meal) => {
    const card = document.getElementById(`meal-${meal.meal_name}`);
    if (!card) return;

    const mealChart = document.getElementById(`meal-chart-${meal.meal_name}`);
    if (mealChart && meal.macros) {
      drawDonutChart(mealChart, meal.macros, {
        size: 74,
        centerLabel: "",
      });
    }

    const calEl = document.getElementById(`meal-cal-${meal.meal_name}`);
    if (calEl && meal.meal_calories) {
      calEl.textContent = `${meal.meal_calories} kcal`;
    }

    const list = card.querySelector(".meal-food-list");
    clearEl(list);
    if (meal.foods.length === 0) {
      const empty = document.createElement("li");
      empty.textContent = "No items.";
      list.appendChild(empty);
      return;
    }
    meal.foods.forEach((food) => {
      const tone = foodToneLookup.get(normalizeFoodKey(food?.name)) ?? "";
      list.appendChild(createFoodCard(food, tone));
    });
  });
}

function renderResults(data) {
  const foodToneLookup = buildFoodToneLookup(data.foods);
  workoutBadge.textContent = data.workout_class;
  loadBadge.textContent    = `${data.training_load_score} / 15`;
  drawDonutChart(macroChart, data.macros, {
    size: 180,
    centerLabel: "Macros",
    legendTarget: macroLegend,
  });
  renderFoods(data);
  renderMealPlan(data.meal_plan, foodToneLookup);
}

// ─── Validation ────────────────────────────────────────────

const VALID_INTENSITIES = ["low", "moderate", "high", "very_high"];

function validateFormData(duration, mileage, pace, intensity, perceivedEffort, calorieTarget) {
  if (!Number.isInteger(duration) || duration < 1 || duration > 600)
    return "Duration must be a whole number between 1 and 600.";
  if (isNaN(mileage) || mileage < 0.1 || mileage > 200)
    return "Distance must be between 0.1 and 200 km.";
  if (isNaN(pace))
    return "Please enter duration and distance first — pace will be calculated automatically.";
  if (pace < 1 || pace > 30)
    return "Pace must be between 1.0 and 30.0 min/km. Adjust duration or distance.";
  if (!VALID_INTENSITIES.includes(intensity))
    return "Please select a valid intensity.";
  if (!Number.isInteger(perceivedEffort) || perceivedEffort < 1 || perceivedEffort > 5)
    return "Please select a perceived effort level.";
  if (!Number.isInteger(calorieTarget) || calorieTarget < 800 || calorieTarget > 6000)
    return "Calorie target must be between 800 and 6000 kcal.";
  return "";
}

function formatApiError(detail) {
  if (typeof detail === "string" && detail.trim()) {
    return detail;
  }

  if (Array.isArray(detail) && detail.length > 0) {
    const first = detail[0];
    if (first && typeof first.msg === "string") {
      const locField = Array.isArray(first.loc) ? first.loc[first.loc.length - 1] : "";
      const fieldLabel = typeof locField === "string"
        ? `${locField.charAt(0).toUpperCase()}${locField.slice(1).replace(/_/g, " ")}`
        : "Input";
      return `${fieldLabel}: ${first.msg}`;
    }
  }

  return "Unable to fetch recommendations from the API.";
}

// ─── API call ──────────────────────────────────────────────

async function analyzeRecovery(duration, mileage, pace, intensity, perceivedEffort, calorieTarget) {
  const response = await fetch(`${API_BASE}/api/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      duration,
      mileage,
      pace,
      intensity,
      perceived_effort: perceivedEffort,
      calorie_target: calorieTarget,
    }),
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(formatApiError(err.detail));
  }

  return response.json();
}

// ─── Form submit ──────────────────────────────────────────

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const duration       = Number.parseInt(durationInput.value, 10);
  const mileage        = parseFloat(mileageInput.value);
  const pace           = parseFloat(paceInput.value);
  const intensity      = intensityInput.value;
  const perceivedEffort = getPerceivedEffort();
  const calorieTarget  = Number.parseInt(calorieTargetInput.value, 10);

  const error = validateFormData(duration, mileage, pace, intensity, perceivedEffort, calorieTarget);
  if (error) {
    setStatus(error, "error");
    return;
  }

  setStatus("Analyzing your workout…");

  try {
    const data = await analyzeRecovery(duration, mileage, pace, intensity, perceivedEffort, calorieTarget);
    renderResults(data);
    setStatus("Recommendations ready.", "success");
  } catch (err) {
    console.error(err);
    setStatus(err instanceof Error && err.message ? err.message : "Could not load recommendations.", "error");
  }
});

function clearResults() {
  // Clear recommendation lists
  Object.values(categoryLists).forEach((el) => clearEl(el));

  // Reset badges and meal cards
  workoutBadge.textContent = "—";
  loadBadge.textContent = "—";
  document.querySelectorAll('.meal-card').forEach((c) => {
    const cal = c.querySelector('.meal-calories');
    if (cal) cal.textContent = '— kcal';
    const list = c.querySelector('.meal-food-list');
    if (list) clearEl(list);
    const chart = c.querySelector('canvas');
    if (chart) {
      const ctx = chart.getContext('2d');
      ctx.clearRect(0, 0, chart.width, chart.height);
    }
  });

  // Clear macro chart and legend
  if (macroChart && macroChart.getContext) {
    const ctx = macroChart.getContext('2d');
    ctx.clearRect(0, 0, macroChart.width, macroChart.height);
  }
  clearEl(macroLegend);

  // Reset status
  setStatus('', 'info');
}

if (resetBtn) {
  resetBtn.addEventListener('click', () => {
    // Reset form inputs to defaults
    durationInput.value = '';
    mileageInput.value = '';
    paceInput.value = '';
    calorieTargetInput.value = '2000';
    intensityIndex = getIntensityIndex('moderate');
    renderIntensityControl();
    document.querySelectorAll('input[name="perceived_effort"]').forEach((el) => el.checked = false);
    document.querySelector('input[name="perceived_effort"][value="3"]').checked = true;

      // Clear URL query parameters so a page refresh doesn't repopulate the form
      try {
        if (window.history && typeof window.history.replaceState === 'function') {
          window.history.replaceState(null, '', window.location.pathname);
        }
      } catch (e) {
        // ignore history errors in older browsers
      }

      clearResults();
  });
}
