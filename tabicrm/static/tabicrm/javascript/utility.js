// From Django documentation how to get the csrf token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Set up a simple regex to check the contents of the post
const textCheck = (value) => {
    const re = /^[a-zA-Z0-9.,!"'?:;\s@#$%^&*()[\]_+={}\-]{2,75}$/
    return re.test(value.trim())
}

const reloadContent = () => {
    location.reload()
}

$(document).ready(function () {
    $('#customersTable').DataTable();
});

$(document).ready(function () {
    $('#contactsTable').DataTable();
});

$(document).ready(function () {
    $('#ticketsTable').DataTable();
});

$(document).ready(function () {
    $('#equipmentTable').DataTable();
});
