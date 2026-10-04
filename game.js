const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

// ====================== СОСТОЯНИЕ ======================
let state = {
  money: GAME_CONFIG.startingMoney,
  energy: GAME_CONFIG.startingEnergy,
  mood: GAME_CONFIG.startingMood,
  level: 1,
  exp: 0,
  ownedBusinesses: [],
  lastCollect: Date.now()
};

const userId = tg.initDataUnsafe?.user?.id || 0;
const userName = tg.initDataUnsafe?.user?.first_name || "Игрок";
const isAdmin = ADMIN_IDS.includes(userId);

// ====================== СОХРАНЕНИЕ ======================
function load() {
  const raw = localStorage.getItem("life_sim_" + userId);
  if (raw) {
    try {
      state = JSON.parse(raw);
    } catch (e) {}
  }
}

function save() {
  localStorage.setItem("life_sim_" + userId, JSON.stringify(state));
}

// ====================== UI ======================
function updateUI() {
  document.getElementById("userName").textContent = userName;
  document.getElementById("level").textContent = state.level;
  document.getElementById("money").textContent = "$" + state.money.toLocaleString();
  document.getElementById("energyValue").textContent = state.energy + "/" + GAME_CONFIG.maxEnergy;
  document.getElementById("moodValue").textContent = state.mood + "/100";
  document.getElementById("energyBar").style.width = (state.energy / GAME_CONFIG.maxEnergy * 100) + "%";
  document.getElementById("moodBar").style.width = state.mood + "%";

  if (isAdmin) {
    document.getElementById("adminBtn").style.display = "inline-block";
  }

  renderJobs();
  renderBusinesses();
  renderOwned();
}

function toast(msg) {
  const el = document.getElementById("toast");
  el.textContent = msg;
  el.classList.add("show");
  setTimeout(() => el.classList.remove("show"), 2200);
}

// ====================== РАБОТЫ ======================
function renderJobs() {
  const list = document.getElementById("jobsList");
  list.innerHTML = "";

  JOBS.forEach(job => {
    const canWork = state.level >= job.level && state.energy >= job.energy;
    const card = document.createElement("div");
    card.className = "job-card";
    card.innerHTML = `
      <div class="job-info">
        <h3>${job.name}</h3>
        <p>${job.desc}</p>
        <div class="req">Ур. ${job.level} · Энергия ${job.energy}</div>
      </div>
      <div class="job-meta">
        <div class="pay">+$${job.pay}</div>
        <button class="btn" style="width:auto;padding:8px 14px;margin:0" 
          ${canWork ? "" : "disabled"}
          onclick="doJob(${job.id})">Работать</button>
      </div>
    `;
    list.appendChild(card);
  });
}

function doJob(id) {
  const job = JOBS.find(j => j.id === id);
  if (!job) return;
  if (state.level < job.level) return toast("Нужен выше уровень");
  if (state.energy < job.energy) return toast("Не хватает энергии");

  state.energy -= job.energy;
  state.money += job.pay;
  state.mood = Math.max(0, Math.min(100, state.mood + job.mood));
  state.exp += Math.floor(job.pay / 10);

  // Level up
  const needExp = state.level * 100;
  if (state.exp >= needExp) {
    state.exp -= needExp;
    state.level++;
    toast(`Уровень повышен! Теперь ${state.level}`);
  } else {
    toast(`+$${job.pay}`);
  }

  save();
  updateUI();
}

// ====================== БИЗНЕСЫ ======================
function renderBusinesses() {
  const list = document.getElementById("businessList");
  list.innerHTML = "";

  BUSINESSES.forEach(biz => {
    const owned = state.ownedBusinesses.includes(biz.id);
    const canBuy = !owned && state.money >= biz.price && state.level >= biz.level;

    const card = document.createElement("div");
    card.className = "biz-card";
    card.innerHTML = `
      <div class="biz-info">
        <h3>${biz.name}</h3>
        <p>${biz.desc}</p>
        <div class="req">Ур. ${biz.level} · Доход $${biz.income}/сбор</div>
      </div>
      <div class="biz-meta">
        <div class="pay">$${biz.price.toLocaleString()}</div>
        <button class="btn" style="width:auto;padding:8px 14px;margin:0"
          ${canBuy ? "" : "disabled"}
          onclick="buyBusiness(${biz.id})">
          ${owned ? "Куплено" : "Купить"}
        </button>
      </div>
    `;
    list.appendChild(card);
  });
}

function buyBusiness(id) {
  const biz = BUSINESSES.find(b => b.id === id);
  if (!biz) return;
  if (state.ownedBusinesses.includes(id)) return toast("Уже куплено");
  if (state.money < biz.price) return toast("Не хватает денег");
  if (state.level < biz.level) return toast("Нужен выше уровень");

  state.money -= biz.price;
  state.ownedBusinesses.push(id);
  toast(`Куплено: ${biz.name}`);
  save();
  updateUI();
}

function renderOwned() {
  const el = document.getElementById("ownedList");
  if (state.ownedBusinesses.length === 0) {
    el.innerHTML = "Пока нет бизнесов";
    return;
  }

  el.innerHTML = state.ownedBusinesses.map(id => {
    const b = BUSINESSES.find(x => x.id === id);
    return `<div style="margin-bottom:8px">• ${b.name} — <span style="color:#22c55e">$${b.income}</span></div>`;
  }).join("");
}

function collectIncome() {
  if (state.ownedBusinesses.length === 0) return toast("Нет бизнесов");

  let total = 0;
  state.ownedBusinesses.forEach(id => {
    const b = BUSINESSES.find(x => x.id === id);
    if (b) total += b.income;
  });

  state.money += total;
  state.lastCollect = Date.now();
  toast(`Собрано $${total.toLocaleString()}`);
  save();
  updateUI();
}

// ====================== ОТДЫХ ======================
function rest() {
  if (state.energy >= GAME_CONFIG.maxEnergy) return toast("Энергия полная");
  state.energy = Math.min(GAME_CONFIG.maxEnergy, state.energy + 25);
  state.mood = Math.min(100, state.mood + 5);
  toast("+25 энергии");
  save();
  updateUI();
}

// ====================== АДМИН ======================
function adminGiveMoney(amount) {
  if (!isAdmin) return;
  state.money += amount;
  toast(`Админ: +$${amount}`);
  save();
  updateUI();
}

function adminSetEnergy(val) {
  if (!isAdmin) return;
  state.energy = val;
  toast("Энергия восстановлена");
  save();
  updateUI();
}

function adminSetMood(val) {
  if (!isAdmin) return;
  state.mood = val;
  toast("Настроение полное");
  save();
  updateUI();
}

function adminReset() {
  if (!isAdmin) return;
  if (!confirm("Сбросить весь прогресс?")) return;
  state = {
    money: GAME_CONFIG.startingMoney,
    energy: GAME_CONFIG.startingEnergy,
    mood: GAME_CONFIG.startingMood,
    level: 1,
    exp: 0,
    ownedBusinesses: [],
    lastCollect: Date.now()
  };
  save();
  updateUI();
  toast("Прогресс сброшен");
}

// ====================== НАВИГАЦИЯ ======================
document.querySelectorAll(".nav-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById("tab-" + btn.dataset.tab).classList.add("active");
  });
});

document.getElementById("restBtn").addEventListener("click", rest);
document.getElementById("collectBtn").addEventListener("click", collectIncome);

// ====================== СТАРТ ======================
load();
updateUI();
