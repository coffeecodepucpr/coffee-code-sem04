let groupsMock = [
  { id: 1, subject: "Mathematics", students: 5, schedule: "monday" },
  { id: 2, subject: "Physics", students: 0, schedule: "tuesday" },
  { id: 3, subject: "Programming", students: 10, schedule: "wednesday" },
  { id: 4, subject: "History", students: 3, schedule: "thursday" },
  { id: 5, subject: "Literature", students: 7, schedule: "friday" },
  { id: 6, subject: "Chemistry", students: 2, schedule: "saturday" },
];

const userMock = {
  name: "John Smith",
  email: "john.smith@supermail.com",
  subjects: [1, 2, 3],
};

// ---------- Reusable components ----------

function createCardHTML(group, action) {
  let buttonLabel;
  if (action === false) { // false means Exit, true means Learn
    buttonLabel = "Exit";
  } else {
    buttonLabel = "Learn";
  }

  let buttonClass;
  if (action === false) {
    buttonClass = "button-secondary";
  } else {
    buttonClass = "button-primary";
  }

  return `
    <article class="card">
      <h3>${group.subject}</h3>
      <p>${group.students} students</p>
      <button class="button ${buttonClass}" type="button" data-id="${group.id}" data-action="${action}">
        ${buttonLabel}
      </button>
    </article>
  `;
}

// no groups

function htmlEmptyState(message) {
  return `<p class="empty-state">${message}</p>`;
}

// ============================================================
// MAIN PAGE (INDEX)
// ============================================================

function iniciateIndex() {
  const container = document.querySelector("#index-grid");
  if (!container) return; // not the Index page

  // Render groups
  function renderGroups(list) {
    if (list.length) { // if list is not empty
      container.innerHTML = list.map((g) => createCardHTML(g, true)).join("");
    } else {  // if list is empty
      container.innerHTML = htmlEmptyState("No groups found.");
    }
  }

  // Click button
  container.addEventListener("click", function (event) {
    const button = event.target.closest("button");
    if (!button) return;
    window.location.href = "login.html";
  });

  renderGroups(groupsMock);
}

// ============================================================
// LOGIN
// ============================================================

function iniciateLogin() {
  const formLogin = document.querySelector("#form-login");
  if(!formLogin) return; // not the Login page

  const fieldEmail = document.querySelector("#email");
  const fieldPass = document.querySelector("#password");
  const errorEmail = document.querySelector("#error-email");
  const errorPass = document.querySelector("#error-pass");
  const messageSuccess = document.querySelector("#message-success");

  formLogin.addEventListener("submit", function (event) {
    event.preventDefault(); // do not reload page

    const email = fieldEmail.value.trim();
    const pass = fieldPass.value;

    errorEmail.textContent = "";
    errorPass.textContent = "";
    messageSuccess.textContent = "";
    let valid = true;
    
    if (!email) {
      errorEmail.textContent = "Enter your e-mail.";
      valid = false;
    } else if (!email.includes("@")) {
      errorEmail.textContent = "Enter correct email.";
      valid = false;
    }

    if (!pass) {
      errorPass.textContent = "Enter your password.";
      valid = false;
    } else if (pass.length < 8) {
      errorPass.textContent = "Password must be at least 8 characters.";
      valid = false;
    }

    if (valid) {
      messageSuccess.textContent = "Valid login!";
      console.log("Valid form:", { email });
    }
  });
}

// ============================================================
// DASHBOARD
// ============================================================

function iniciateDashboard() {
  const container = document.querySelector("#dashboard-grid");
  if (!container) return; // not the Dashboard page

  // Render groups
  function renderGroups(list) {
    if (list.length) { // if list is not empty
      container.innerHTML = list.map((g) => createCardHTML(g, true)).join("");
    } else {  // if list is empty
      container.innerHTML = htmlEmptyState("No groups found.");
    }
  }  

  // Search
  const searchField = document.querySelector("#search");
  if (searchField) {
    searchField.addEventListener("input", function (event) {
      const typedWord = event.target.value.trim().toLowerCase();
      const filteredGroups = groupsMock.filter(function(g) {
        return g.subject.toLowerCase().includes(typedWord);
      });
      renderGroups(filteredGroups);
    });
  }

  // Click Learn button
  container.addEventListener("click", function (event) {
    const button = event.target.closest("button");
    if (!button) return;
    console.log("Learn clicked, group id:", button.dataset.id);
  });

  // New group add
  const containerButtonNew = document.querySelector("#button-new-group");
  if (containerButtonNew) {
    containerButtonNew.addEventListener("click", function () {
      const groupId = Number(event.target.dataset.id);
      newGroup = { subject: "NewGroup", students: 10 };
      
      function addGroup(newGroup) {
        const groupToAdd = {
          id: Date.now(),
          subject: newGroup.subject,
          students: newGroup.students
        };
          
        groupsMock.push(groupToAdd);
        renderGroups(groupsMock);
      }

      addGroup(newGroup);
    });
  }

  renderGroups(groupsMock);
}

// ============================================================
// PROFILE
// ============================================================

function iniciateProfile() {
  const containerProfile = document.querySelector("#profile-grid");
  if (!containerProfile) return; // not the Profile page

  const nameEl = document.querySelector("#profile-name");
  const emailEl = document.querySelector("#profile-email");
  const tagsEl = document.querySelector("#profile-tags");
  const countEl = document.querySelector("#profile-count");

  const { name, email } = userMock;

  nameEl.textContent = name;
  emailEl.textContent = email;

  function myGroups() {
    return groupsMock.filter((g) => userMock.subjects.includes(g.id));
  }

  function renderTags(list) {
    tagsEl.innerHTML = list.map((g) => `<span class="tag">${g.subject}</span>`).join("");
  }

  function renderMyGroups() {
    const list = myGroups();
    countEl.textContent = `You are in ${list.length} group${list.length === 1 ? "" : "s"}.`;
    if (list.length) {
      containerProfile.innerHTML = list.map((g) => createCardHTML(g, false)).join("");
    } else {
      containerProfile.innerHTML = htmlEmptyState("You have no groups.");
    }
    renderTags(list);
  }  

  function exitGroup(id) {
    console.log("exitGroup in");
    userMock.subjects = userMock.subjects.filter((subjectId) => subjectId !== id);
    renderMyGroups();
  }

  containerProfile.addEventListener("click", function (event) {
    const button = event.target.closest("button");
    if (!button) return;
    exitGroup(Number(button.dataset.id));
  });

  renderMyGroups();
}

// ============================================================
// Entry point
// ============================================================

iniciateLogin();
iniciateDashboard();
iniciateProfile();
iniciateIndex();
