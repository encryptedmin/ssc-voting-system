document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-auto-dismiss="true"]').forEach((alert, index) => {
        window.setTimeout(() => {
            alert.classList.add('alert-fading');

            window.setTimeout(() => {
                if (window.bootstrap) {
                    bootstrap.Alert.getOrCreateInstance(alert).close();
                } else {
                    alert.remove();
                }
            }, 1200);
        }, 3500 + (index * 300));
    });
});
