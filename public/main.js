const navigation = document.getElementById("myNav");
const menuButton = document.getElementById("menuButton");
const closeButton = document.getElementById("closeNavButton");
const peopleContainer = document.getElementById("people");

function openNav() {
  navigation.style.width = "100%";
  menuButton.classList.add("change");
}

function closeNav() {
  navigation.style.width = "0%";
  menuButton.classList.remove("change");
}

function createPersonCard(person) {
  const section = document.createElement("section");
  section.className = "person-card";

  const yearMarkup = person.date
    ? `<p class="person-card-year">Born ${person.date}</p>`
    : "";

  section.innerHTML = `
    <div class="person-card-inner">
      <img class="person-card-image" src="${person.image}" alt="${person.name.trim()}">
      <div class="person-card-copy">
        ${yearMarkup}
        <h2 class="person-card-title">${person.name.trim()}</h2>
        <p class="person-card-description">${person.description}</p>
      </div>
    </div>
  `;

  return section;
}

async function fetchPeople() {
  const response = await fetch("data/accurate_people.json");

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.json();
}

async function renderPeople() {
  try {
    const people = await fetchPeople();
    const fragment = document.createDocumentFragment();

    people.forEach((person) => {
      fragment.appendChild(createPersonCard(person));
    });

    peopleContainer.replaceChildren(fragment);
  } catch (error) {
    peopleContainer.innerHTML = `
      <section class="person-card person-card-error">
        <div class="person-card-inner">
          <div class="person-card-copy">
            <p class="person-card-year">Data unavailable</p>
            <h2 class="person-card-title">Unable to load people</h2>
            <p class="person-card-description">Please try again in a moment.</p>
          </div>
        </div>
      </section>
    `;
    console.error(error);
  }
}

menuButton.addEventListener("click", () => {
  if (navigation.style.width === "100%") {
    closeNav();
    return;
  }

  openNav();
});

closeButton.addEventListener("click", (event) => {
  event.preventDefault();
  closeNav();
});

renderPeople();
