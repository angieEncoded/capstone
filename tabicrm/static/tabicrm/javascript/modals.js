const showConfirmDeleteModal = () => {
    // create the modal
    let confirmModal = new bootstrap.Modal(document.getElementById('confirmDelete'), {
        keyboard: false,
        backdrop: 'static'
    })
    confirmModal.show()
}

const showNewContactFormModal = () => {
    let newContactModal = new bootstrap.Modal(document.getElementById('addContactModal'), {
        keyboard: false,
        backdrop: 'static'
    })
    newContactModal.show()
}

const showNewLicenseFormModal = () => {
    let newContactModal = new bootstrap.Modal(document.getElementById('addLicenseModal'), {
        keyboard: false,
        backdrop: 'static'
    })
    newContactModal.show()
}

const showNewEquipmentFormModal = () => {
    let newEquipmentModal = new bootstrap.Modal(document.getElementById('addEquipmentModal'), {
        keyboard: false,
        backdrop: 'static'
    })
    newEquipmentModal.show()
}

const showNewTicketFormModal = () => {
    let newTicketModal = new bootstrap.Modal(document.getElementById('addTicketModal'), {
        keyboard: false,
        backdrop: 'static'
    })
    newTicketModal.show()
}

const openTicketModal = () => {
    let ticketModal = new bootstrap.Modal(document.getElementById('editTicketModal'), {
        keyboard: false,
        backdrop: 'static'
    })
    ticketModal.show()
}

const openHistoryModal = () => {
    let ticketHistoryModal = new bootstrap.Modal(document.getElementById('ticketHistoryModal'), {
        keyboard: false,
        backdrop: 'static'
    })
    ticketHistoryModal.show()
}

const openFullEditForm = () => {
    document.querySelector("#customer-simple-view").style.display = "none"
    document.querySelector("#customer-full-edit-form").style.display = "block"
}

const closeFullEditForm = () => {
    document.querySelector("#customer-simple-view").style.display = "block"
    document.querySelector("#customer-full-edit-form").style.display = "none"
}