document.addEventListener("DOMContentLoaded", function () {
    const sections = document.querySelectorAll(".form-section");
    const nextBtns = document.querySelectorAll(".next-btn");
    const prevBtns = document.querySelectorAll(".prev-btn");

    let currentSection = 0;

    function showSection(index) {
        sections.forEach((section, i) => {
            section.classList.toggle("active", i === index);
        });
    }

    nextBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            if (currentSection < sections.length - 1) {
                currentSection++;
                showSection(currentSection);
            }
        });
    });

    prevBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            if (currentSection > 0) {
                currentSection--;
                showSection(currentSection);
            }
        });
    });

    document.getElementById('multiSectionForm').addEventListener('submit', function(event) {
        event.preventDefault();
        let formData = new FormData(this);
        fetch('/submit_form', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            alert(data.message);
            this.reset();
        })
        .catch(error => {
            console.error('Error submitting form:', error);
            alert('Error submitting form: ' + error.message);
        });
    });

    showSection(currentSection);
});

function addChildrenFields() {
    var numberOfChildren = document.getElementById('number_of_children').value;
    var container = document.getElementById('children-details-container');
    container.innerHTML = ''; // Clear previous content

    for (var i = 1; i <= numberOfChildren; i++) {
      var childNameLabel = document.createElement('label');
      childNameLabel.textContent = 'Child ' + i + ' Name:';
      container.appendChild(childNameLabel);

      var childNameInput = document.createElement('input');
      childNameInput.type = 'text';
      childNameInput.name = 'child_name_' + i;
      container.appendChild(childNameInput);

      container.appendChild(document.createElement('br')); // Line break

      var childDOBLabel = document.createElement('label');
      childDOBLabel.textContent = 'Child ' + i + ' Date of Birth:';
      container.appendChild(childDOBLabel);

      var childDOBInput = document.createElement('input');
      childDOBInput.type = 'date';
      childDOBInput.name = 'child_dob_' + i;
      container.appendChild(childDOBInput);

      container.appendChild(document.createElement('br')); // Line break
      container.appendChild(document.createElement('br')); // Line break
    }
  }

  function toggleInput(field, container) { 
    if (container.id === "healthydelContainer") {
        if (field.value === "no") {
            container.style.display = "block";
        } else {
            container.style.display = "none";
        }
    }
    else if (container.id === "housingContainer") {
        if (field.value === "community housing") {
            container.style.display = "block";
        } else {
            container.style.display = "none";
        }
    }
    else {
    if (field.value === "yes") {
        container.style.display = "block";
    } else {
        container.style.display = "none";
    }
    }
  }

  document.getElementById('passwordForm').onsubmit = function(e) {
    e.preventDefault();  // Prevent the form from submitting the default way
    var form = e.target;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', form.action, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        if (xhr.status === 200) {
            // Redirect to the client_details page
            window.location.href = '/client_details';
        } else {
            // Display the error message
            document.body.innerHTML = xhr.responseText;
        }
    };
    xhr.send(new URLSearchParams(new FormData(form)).toString());

};