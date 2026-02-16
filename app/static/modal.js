let formToSubmit = null;

const modal = document.getElementById("confirmDeleteModal");
const modalMessage = document.getElementById("modalDeleteMessage");
const modalConfirm = document.getElementById("modalConfirmDelete");

modal.addEventListener("show.bs.modal", (event) => {
  const button = event.relatedTarget;
  const formId = button.getAttribute("data-form-id");
  const itemName = button.getAttribute("data-item-name") || "this item";
  formToSubmit = document.getElementById(formId);
  modalMessage.textContent = `Are you sure you want to delete ${itemName}?`;
});

modalConfirm.addEventListener("click", () => {
  if (formToSubmit) {
    formToSubmit.submit();
  }
});
