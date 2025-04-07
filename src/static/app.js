document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");
const darkModeToggle = document.getElementById("dark-mode-toggle");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Clear existing options in the dropdown
      activitySelect.innerHTML = "<option value=''>-- Select an activity --</option>";

      // Populate activities list
      activities.forEach((details) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        if (spotsLeft <= 0) {
          activityCard.classList.add("full");
          activityCard.innerHTML = `<h4>${details.name} (FULL)</h4>`;
          activitiesList.appendChild(activityCard);
          return;
        }

        // Create participants list with delete icons
        const participantsList = details.participants && details.participants.length > 0
          ? `<div class="participants">
               <strong>Participants:</strong>
               <ul style="list-style-type: none; padding: 0;">
                 ${details.participants.map(participant => `
                   <li style="display: flex; align-items: center;">
                     <span>${participant}</span>
                     <button class="delete-participant" data-activity="${details.name}" data-participant="${participant}" style="margin-left: auto; background: none; border: none; color: red; cursor: pointer;">❌</button>
                   </li>`).join("")}
               </ul>
             </div>`
          : "<p>No participants yet.</p>";

        activityCard.innerHTML = `
          <h4>${details.name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          ${participantsList}
        `;

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = details.name;
        option.textContent = details.name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();

        
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
      // Refresh activities list to update availability
    await fetchActivities();
  });

// Toggle dark mode
  darkModeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    document.querySelector("header").classList.toggle("dark-mode");
    document.querySelectorAll("section").forEach(section => {
      section.classList.toggle("dark-mode");
    });

    // Update button text
    if (document.body.classList.contains("dark-mode")) {
      darkModeToggle.textContent = "☀️ Light Mode";
    } else {
      darkModeToggle.textContent = "🌙 Dark Mode";
    }
  });

// Event listener for delete participant buttons
document.addEventListener("click", async (event) => {
  if (event.target.classList.contains("delete-participant")) {
    const activity = event.target.getAttribute("data-activity");
    const participant = event.target.getAttribute("data-participant");

    try {
      const response = await fetch(`/activities/${encodeURIComponent(activity)}/unregister?email=${encodeURIComponent(participant)}`, {
        method: "DELETE",
      });

      if (response.ok) {
        alert("Participant unregistered successfully.");
        await fetchActivities(); // Refresh activities list
      } else {
        alert("Failed to unregister participant.");
      }
    } catch (error) {
      console.error("Error unregistering participant:", error);
      alert("An error occurred while trying to unregister the participant.");
    }
  }
});

// Initialize app
  fetchActivities();
});
