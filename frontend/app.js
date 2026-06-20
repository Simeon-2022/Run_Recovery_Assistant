"use strict";

const API_BASE = "http://127.0.0.1:8000";

const form = document.getElementById("recovery-form");
const durationInput = document.getElementById("duration");
const intensityInput = document.getElementById("intensity");
const statusMessage = document.getElementById("form-message");
const workoutClassBadge = document.getElementById("workout-class");

const categoryLists = {
  carbs: document.getElementById("carbs-list"),
  protein: document.getElementById("protein-list"),
  antioxidants: document.getElementById("antioxidants-list"),
};

Object.entries(categoryLists).forEach(([category, list]) => {
  list.dataset.tone = category;
});

function clearResults() {
  Object.values(categoryLists).forEach((list) => {
    while (list.firstChild) {
      list.removeChild(list.firstChild);
    }
  });
}

function setStatus(message) {
  statusMessage.textContent = message;
}

function addFoodCard(listElement, food) {
  const listItem = document.createElement("li");

  const name = document.createElement("strong");
  name.textContent = food.name;

  const description = document.createElement("span");
  description.textContent = food.description;

  const nutrients = document.createElement("small");
  nutrients.textContent = `Nutrients: ${food.nutrients_summary}`;

  listItem.appendChild(name);
  listItem.appendChild(description);
  listItem.appendChild(nutrients);

  listElement.appendChild(listItem);
}

function validateFormData(duration, intensity) {
  if (!Number.isInteger(duration) || duration < 1 || duration > 600) {
    return "Duration must be a whole number between 1 and 600.";
  }

  const allowedIntensities = ["low", "medium", "high"];
  if (!allowedIntensities.includes(intensity)) {
    return "Intensity must be low, medium, or high.";
  }

  return "";
}

async function analyzeRecovery(duration, intensity) {
  const response = await fetch(`${API_BASE}/api/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ duration, intensity }),
  });

  if (!response.ok) {
    throw new Error("Unable to fetch recommendations from the API.");
  }

  return response.json();
}

function renderResults(data) {
  workoutClassBadge.textContent = data.workout_class;
  clearResults();

  Object.entries(categoryLists).forEach(([category, listElement]) => {
    const foods = data.foods?.[category] ?? [];
    if (foods.length === 0) {
      const emptyState = document.createElement("li");
      emptyState.textContent = "No items found for this category yet.";
      listElement.appendChild(emptyState);
      return;
    }

    foods.forEach((food) => addFoodCard(listElement, food));
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const duration = Number.parseInt(durationInput.value, 10);
  const intensity = intensityInput.value;

  const validationMessage = validateFormData(duration, intensity);
  if (validationMessage) {
    setStatus(validationMessage);
    return;
  }

  setStatus("Analyzing your workout...");

  try {
    const data = await analyzeRecovery(duration, intensity);
    renderResults(data);
    setStatus("Recommendations ready.");
  } catch (error) {
    console.error(error);
    setStatus("Could not load recommendations. Ensure the backend API is running.");
  }
});
