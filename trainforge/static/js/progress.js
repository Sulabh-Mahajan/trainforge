/* ═══════════════════════════════════════════════
   Manual data right now, will use database later
═══════════════════════════════════════════════ */
const CLIENTS = [
    {
        name: "Alex Mitchell",
        initials: "AM",
        color: "#C0202A",
        bg: "#FCEAEA",
        goal: "Strength",
        sessions: 18,
        exercises: [
            {
                name: "Bench Press",
                unit: "kg",
                weeks: ["Wk1", "Wk2", "Wk3", "Wk4", "Wk5", "Wk6"],
                data: [60, 65, 65, 70, 72, 75],
                trend: "+15kg",
            },
            {
                name: "Squat",
                unit: "kg",
                weeks: ["Wk1", "Wk2", "Wk3", "Wk4", "Wk5", "Wk6"],
                data: [80, 82, 85, 88, 90, 95],
                trend: "+15kg",
            },
            {
                name: "Deadlift",
                unit: "kg",
                weeks: ["Wk1", "Wk2", "Wk3", "Wk4", "Wk5", "Wk6"],
                data: [100, 105, 105, 110, 115, 120],
                trend: "+20kg",
            },
            {
                name: "Pull-ups",
                unit: "reps",
                weeks: ["Wk1", "Wk2", "Wk3", "Wk4", "Wk5", "Wk6"],
                data: [5, 6, 7, 7, 9, 10],
                trend: "+5 reps",
            },
        ],
    },
    {
        name: "Sarah Kim",
        initials: "SK",
        color: "#185FA5",
        bg: "#E6F1FB",
        goal: "Weight Loss",
        sessions: 14,
        exercises: [
            {
                name: "Treadmill",
                unit: "km",
                weeks: ["Wk1", "Wk2", "Wk3", "Wk4", "Wk5", "Wk6"],
                data: [2, 2.5, 3, 3.5, 4, 4.5],
                trend: "+2.5km",
            },
            {
                name: "Rowing",
                unit: "cal",
                weeks: ["Wk1", "Wk2", "Wk3", "Wk4", "Wk5", "Wk6"],
                data: [150, 170, 190, 200, 220, 240],
                trend: "+90cal",
            },
            {
                name: "Jump Rope",
                unit: "min",
                weeks: ["Wk1", "Wk2", "Wk3", "Wk4", "Wk5", "Wk6"],
                data: [5, 6, 8, 9, 10, 12],
                trend: "+7min",
            },
            {
                name: "Cycling",
                unit: "km",
                weeks: ["Wk1", "Wk2", "Wk3", "Wk4", "Wk5", "Wk6"],
                data: [8, 9, 11, 12, 14, 15],
                trend: "+7km",
            },
        ],
    },
    {
        name: "James Park",
        initials: "JP",
        color: "#0F6E56",
        bg: "#E1F5EE",
        goal: "Mobility",
        sessions: 22,
        exercises: [
            {
                name: "Hip Flexor",
                unit: "sec",
                weeks: ["Wk1", "Wk2", "Wk3", "Wk4", "Wk5", "Wk6"],
                data: [20, 25, 30, 35, 40, 45],
                trend: "+25sec",
            },
            {
                name: "Shoulder ROM",
                unit: "deg",
                weeks: ["Wk1", "Wk2", "Wk3", "Wk4", "Wk5", "Wk6"],
                data: [100, 108, 115, 120, 128, 135],
                trend: "+35°",
            },
            {
                name: "Hamstring",
                unit: "cm",
                weeks: ["Wk1", "Wk2", "Wk3", "Wk4", "Wk5", "Wk6"],
                data: [5, 8, 10, 12, 15, 18],
                trend: "+13cm",
            },
        ],
    },
    {
        name: "Emma Davis",
        initials: "ED",
        color: "#BA7517",
        bg: "#FAEEDA",
        goal: "Cardio",
        sessions: 10,
        exercises: [
            {
                name: "5K Run",
                unit: "min",
                weeks: ["Wk1", "Wk2", "Wk3", "Wk4", "Wk5", "Wk6"],
                data: [38, 36, 35, 33, 31, 30],
                trend: "-8min",
            },
            {
                name: "VO2 Score",
                unit: "pts",
                weeks: ["Wk1", "Wk2", "Wk3", "Wk4", "Wk5", "Wk6"],
                data: [28, 30, 31, 33, 34, 36],
                trend: "+8pts",
            },
            {
                name: "Stair Climber",
                unit: "min",
                weeks: ["Wk1", "Wk2", "Wk3", "Wk4", "Wk5", "Wk6"],
                data: [8, 10, 12, 14, 15, 18],
                trend: "+10min",
            },
        ],
    },
    {
        name: "Marcus Reid",
        initials: "MR",
        color: "#533AB7",
        bg: "#EEEDFE",
        goal: "Strength",
        sessions: 16,
        exercises: [
            {
                name: "Overhead Press",
                unit: "kg",
                weeks: ["Wk1", "Wk2", "Wk3", "Wk4", "Wk5", "Wk6"],
                data: [40, 42, 44, 46, 48, 50],
                trend: "+10kg",
            },
            {
                name: "Barbell Row",
                unit: "kg",
                weeks: ["Wk1", "Wk2", "Wk3", "Wk4", "Wk5", "Wk6"],
                data: [55, 58, 60, 63, 65, 68],
                trend: "+13kg",
            },
            {
                name: "Dips",
                unit: "reps",
                weeks: ["Wk1", "Wk2", "Wk3", "Wk4", "Wk5", "Wk6"],
                data: [8, 9, 10, 12, 13, 15],
                trend: "+7 reps",
            },
        ],
    },
];

/* ═══════════════════════════════════════════════
   DOM REFS
═══════════════════════════════════════════════ */
const searchInput     = document.getElementById("searchInput");
const goalFilter      = document.getElementById("goalFilter");
const clientDropdown  = document.getElementById("clientDropdown");
const clientBanner    = document.getElementById("clientBanner");
const bannerAvatar    = document.getElementById("bannerAvatar");
const bannerName      = document.getElementById("bannerName");
const bannerMeta      = document.getElementById("bannerMeta");
const bannerBadge     = document.getElementById("bannerBadge");
const clearBtn        = document.getElementById("clearBtn");
const progressSection = document.getElementById("progressSection");
const progressTitle   = document.getElementById("progressTitle");
const chartsGrid      = document.getElementById("chartsGrid");
const emptyState      = document.getElementById("emptyState");

/* ═══════════════════════════════════════════════
   STATE
═══════════════════════════════════════════════ */
let chartInstances = [];
let activeClient   = null;

/* ═══════════════════════════════════════════════
   DATE
═══════════════════════════════════════════════ */
document.getElementById("todayDate").textContent =
    new Date().toLocaleDateString("en-AU", {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric",
    });

/* ═══════════════════════════════════════════════
   MOBILE SIDEBAR TOGGLE
═══════════════════════════════════════════════ */
const sidebar        = document.getElementById("sidebar");
const sidebarOverlay = document.getElementById("sidebarOverlay");
const sidebarToggle  = document.getElementById("sidebarToggle");

if (sidebarToggle) {
    sidebarToggle.addEventListener("click", () => {
        sidebar.classList.toggle("sidebar-open");
        sidebarOverlay.classList.toggle("active");
    });
    sidebarOverlay.addEventListener("click", () => {
        sidebar.classList.remove("sidebar-open");
        sidebarOverlay.classList.remove("active");
    });
}

/* ═══════════════════════════════════════════════
   SEARCH / DROPDOWN
═══════════════════════════════════════════════ */
function getFilteredClients(query) {
    const goal = goalFilter.value;
    return CLIENTS.filter((c) => {
        const matchGoal  = !goal || c.goal === goal;
        const matchQuery = !query || c.name.toLowerCase().includes(query.toLowerCase());
        return matchGoal && matchQuery;
    });
}

function renderDropdown(query) {
    const results = getFilteredClients(query);
    clientDropdown.innerHTML = "";

    if (!results.length) {
        clientDropdown.innerHTML = '<div class="dd-empty">No clients found</div>';
    } else {
        results.forEach((c) => {
            const item = document.createElement("div");
            item.className = "dd-item d-flex align-items-center gap-2";
            item.innerHTML = `
                <div class="client-avatar" style="background:${c.bg};color:${c.color};">${c.initials}</div>
                <span>${c.name}</span>
                <span class="ms-auto text-secondary" style="font-size:0.75rem;">${c.goal}</span>`;
            item.addEventListener("mousedown", (e) => {
                e.preventDefault();
                selectClient(c);
            });
            clientDropdown.appendChild(item);
        });
    }
    clientDropdown.classList.add("open");
}

searchInput.addEventListener("input", () => {
    const q = searchInput.value.trim();
    if (q) renderDropdown(q);
    else clientDropdown.classList.remove("open");
});

searchInput.addEventListener("focus", () => {
    if (searchInput.value.trim()) renderDropdown(searchInput.value.trim());
});

searchInput.addEventListener("blur", () => {
    setTimeout(() => clientDropdown.classList.remove("open"), 150);
});

goalFilter.addEventListener("change", () => {
    if (searchInput.value.trim()) renderDropdown(searchInput.value.trim());
});

/* ═══════════════════════════════════════════════
   SELECT / CLEAR CLIENT
═══════════════════════════════════════════════ */
function selectClient(client) {
    activeClient = client;
    searchInput.value = client.name;
    clientDropdown.classList.remove("open");

    // Banner
    bannerAvatar.textContent       = client.initials;
    bannerAvatar.style.background  = client.bg;
    bannerAvatar.style.color       = client.color;
    bannerName.textContent         = client.name;
    bannerMeta.textContent         = `${client.sessions} sessions · ${client.goal}`;
    bannerBadge.textContent        = client.goal;
    bannerBadge.style.background   = client.bg;
    bannerBadge.style.color        = client.color;
    clientBanner.style.display     = "block";

    renderCharts(client);
}

clearBtn.addEventListener("click", () => {
    activeClient               = null;
    searchInput.value          = "";
    clientBanner.style.display = "none";

    // FIX: use style.display — classList "visible" cannot override inline style="display:none"
    progressSection.style.display = "none";
    emptyState.style.display      = "block";

    chartInstances.forEach((c) => c.destroy());
    chartInstances   = [];
    chartsGrid.innerHTML = "";
});

/* ═══════════════════════════════════════════════
   RENDER CHARTS
═══════════════════════════════════════════════ */
function renderCharts(client) {
    chartInstances.forEach((c) => c.destroy());
    chartInstances   = [];
    chartsGrid.innerHTML = "";

    progressTitle.textContent = `${client.name}'s exercise progress`;

    // FIX: use style.display — classList "visible" cannot override inline style="display:none"
    progressSection.style.display = "block";
    emptyState.style.display      = "none";

    client.exercises.forEach((ex, i) => {
        const first    = ex.data[0];
        const last     = ex.data[ex.data.length - 1];
        const improving = last >= first;

        const col = document.createElement("div");
        col.className = "col-12 col-md-6 col-xl-3";
        col.innerHTML = `
            <div class="dash-card h-100">
                <p class="fw-semibold mb-1" style="font-size:0.83rem;color:#1a1a1a;">${ex.name}</p>
                <p class="text-secondary mb-3" style="font-size:0.72rem;">Last 6 weeks · ${ex.unit}</p>
                <div class="chart-wrap">
                    <canvas id="chart_${i}" role="img" aria-label="${ex.name} progress for ${client.name}"></canvas>
                </div>
                <div class="d-flex gap-2 mt-3">
                    <div class="stat-pill">
                        <div class="val">${first}</div>
                        <div class="lbl">Start</div>
                    </div>
                    <div class="stat-pill">
                        <div class="val">${last}</div>
                        <div class="lbl">Now</div>
                    </div>
                    <div class="stat-pill">
                        <div class="val" style="color:${improving ? "#0F6E56" : "#C0202A"};">${ex.trend}</div>
                        <div class="lbl">Change</div>
                    </div>
                </div>
            </div>`;

        chartsGrid.appendChild(col);

        requestAnimationFrame(() => {
            const ctx  = document.getElementById(`chart_${i}`).getContext("2d");
            const inst = new Chart(ctx, {
                type: "line",
                data: {
                    labels: ex.weeks,
                    datasets: [{
                        label: ex.unit,
                        data: ex.data,
                        borderColor: client.color,
                        backgroundColor: client.bg + "BB",
                        borderWidth: 2,
                        fill: true,
                        tension: 0.38,
                        pointRadius: 4,
                        pointBackgroundColor: client.color,
                        pointBorderColor: "#fff",
                        pointBorderWidth: 2,
                    }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: (ctx) => `${ctx.parsed.y} ${ex.unit}`,
                            },
                        },
                    },
                    scales: {
                        x: {
                            grid: { color: "rgba(0,0,0,0.04)" },
                            ticks: {
                                font: { size: 11 },
                                color: "#adb5bd",
                                autoSkip: false,
                                maxRotation: 0,
                            },
                        },
                        y: {
                            grid: { color: "rgba(0,0,0,0.04)" },
                            ticks: {
                                font: { size: 11 },
                                color: "#adb5bd",
                            },
                            beginAtZero: false,
                        },
                    },
                },
            });
            chartInstances.push(inst);
        });
    });
}
