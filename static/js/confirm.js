let formToConfirm = null;

document.addEventListener("DOMContentLoaded", function () {
    const confirmBox = document.getElementById("global-confirm");
    const confirmYes = document.getElementById("confirm-yes");
    const confirmNo = document.getElementById("confirm-no");
    const confirmMsg = document.getElementById("confirm-message");

    document.querySelectorAll("[data-confirm]").forEach(btn => {
        btn.addEventListener("click", function () {
            const message = this.dataset.confirm || "Are you sure?";
            confirmMsg.textContent = message;
            formToConfirm = this.closest("form");
            confirmBox.style.display = "flex";
        });
    });

    confirmYes.addEventListener("click", () => {
        if (formToConfirm) formToConfirm.submit();
    });

    confirmNo.addEventListener("click", () => {
        confirmBox.style.display = "none";
        formToConfirm = null;
    });
});
