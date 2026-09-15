// Sidebar toggle
document.getElementById("sidebarToggle").addEventListener("click", () => {
    document.getElementById("sidebar").classList.toggle("sidebar-open");
    document.getElementById("sidebarOverlay").classList.toggle("active");
});
document.getElementById("sidebarOverlay").addEventListener("click", () => {
    document.getElementById("sidebar").classList.remove("sidebar-open");
    document.getElementById("sidebarOverlay").classList.remove("active");
});

// ── VIEW SWITCHING ──
function showCreateForm() {
    document.getElementById("plansView").classList.add("d-none");
    document.getElementById("createFormView").classList.remove("d-none");
    window.scrollTo({ top: 0, behavior: "smooth" });
}

function showPlansView() {
    document.getElementById("createFormView").classList.add("d-none");
    document.getElementById("plansView").classList.remove("d-none");
    window.scrollTo({ top: 0, behavior: "smooth" });
}

// ── EXERCISE BUILDER ──
let exerciseCount = 1;

function addExercise() {
    exerciseCount++;
    const id = `exercise-${exerciseCount}`;
    const html = `
                    <div class="exercise-row" id="${id}">
                        <div class="exercise-row-header d-flex align-items-center justify-content-between mb-2">
                            <span class="exercise-number">Exercise ${exerciseCount}</span>
                            <button class="btn btn-remove-exercise" onclick="removeExercise('${id}')">
                                <i class="bi bi-trash3"></i>
                            </button>
                        </div>
                        <div class="row g-2">
                            <div class="col-12 col-md-4">
                                <input type="text" class="form-control plan-input" placeholder="Exercise name" name="exercise_name"/>
                            </div>
                            <div class="col-6 col-md-2">
                                <input type="number" class="form-control plan-input" placeholder="Sets" min="1" name="sets"/>
                            </div>
                            <div class="col-6 col-md-2">
                                <input type="text" class="form-control plan-input" placeholder="Reps / Duration" name="reps"/>
                            </div>
                            <div class="col-6 col-md-2">
                                <input type="text" class="form-control plan-input" placeholder="Rest (e.g. 60s)" name="rest"/>
                            </div>
                            <div class="col-6 col-md-2">
                                <input type="text" class="form-control plan-input" placeholder="Weight (optional)" name="weight"/>
                            </div>
                            <div class="col-12">
                                <input type="text" class="form-control plan-input" placeholder="Notes (e.g. keep core tight)" name="notes"/>
                            </div>
                        </div>
                    </div>`;
    document
        .getElementById("exerciseList")
        .insertAdjacentHTML("beforeend", html);
    updateExerciseButtons();
}

function removeExercise(id) {
    document.getElementById(id).remove();
    renumberExercises();
    updateExerciseButtons();
}

function renumberExercises() {
    document.querySelectorAll(".exercise-number").forEach((el, i) => {
        el.textContent = `Exercise ${i + 1}`;
    });
}

function updateExerciseButtons() {
    const rows = document.querySelectorAll(".exercise-row");
    rows.forEach((row, i) => {
        const btn = row.querySelector(".btn-remove-exercise");
        btn.disabled = rows.length === 1;
    });
}

function savePlan() {
    const name = document.getElementById("planName").value.trim();
    if (!name) {
        document.getElementById("planName").focus();
        return;
    }
    showPlansView();
}

// ── ASSIGN PANEL ──
const planNames = {
    power: "8-Week Power Program",
    cut: "8-Week Cut Program",
    flex: "6-Week Flex & Mobility",
    "5k": "5K Training Plan",
};

const clients = [
    "Alex Mitchell",
    "Sarah Kim",
    "James Park",
    "Emma Davis",
    "Marcus Reid",
    "Lisa Thompson",
    "Daniel Wong",
    "Priya Nair",
    "Tom Harris",
    "Chloe Laurent",
    "Ryan O'Brien",
    "Nina Foster",
];

function openAssignPanel(planId) {
    const panel = document.getElementById("assignPanel");
    const overlay = document.getElementById("panelOverlay");
    const body = document.getElementById("assignPanelBody");
    const planName = planNames[planId] || "Training Plan";

    body.innerHTML = `
                    <div class="panel-section-title mb-3">Selected Plan</div>
                    <div class="assign-plan-badge mb-4">
                        <i class="bi bi-clipboard2-pulse-fill me-2"></i>${planName}
                    </div>
                    <div class="panel-section-title mb-3">Select Client</div>
                    <div class="d-flex flex-column gap-2" id="clientList">
                        ${clients
                            .map(
                                (c) => `
                            <label class="assign-client-row">
                                <div class="d-flex align-items-center gap-3">
                                    <div class="assign-avatar">${c
                                        .split(" ")
                                        .map((w) => w[0])
                                        .join("")}</div>
                                    <span class="fw-medium" style="font-size:0.875rem">${c}</span>
                                </div>
                                <input type="radio" name="assignClient" value="${c}" class="form-check-input assign-radio"/>
                            </label>`,
                            )
                            .join("")}
                    </div>
                    <div class="mt-4 d-flex flex-column gap-2">
                        <button class="btn btn-panel-primary w-100">
                            <i class="bi bi-person-check me-2"></i>Assign Plan
                        </button>
                        <button class="btn btn-panel-outline w-100" onclick="closeAssignPanel()">Cancel</button>
                    </div>`;

    panel.classList.add("panel-open");
    overlay.classList.add("active");
}

function closeAssignPanel() {
    document.getElementById("assignPanel").classList.remove("panel-open");
    document.getElementById("panelOverlay").classList.remove("active");
}

// ── SEARCH + FILTER ──
function filterPlans() {
    const search = document.getElementById("planSearch").value.toLowerCase();
    const goal = document.getElementById("goalFilter").value;
    document.querySelectorAll(".plan-col").forEach((col) => {
        const name = col
            .querySelector(".plan-card-name")
            .textContent.toLowerCase();
        const colGoal = col.dataset.goal;
        const matchS = name.includes(search);
        const matchG = !goal || colGoal === goal;
        col.style.display = matchS && matchG ? "" : "none";
    });
}

document.getElementById("planSearch").addEventListener("input", filterPlans);
document.getElementById("goalFilter").addEventListener("change", filterPlans);
