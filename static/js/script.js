document.addEventListener(
    "DOMContentLoaded",
    function () {

        // Password confirmation
        const password =
            document.getElementById("password");

        const confirmPassword =
            document.getElementById(
                "confirm_password"
            );


        if (password && confirmPassword) {

            confirmPassword.addEventListener(
                "input",
                function () {

                    if (
                        password.value !==
                        confirmPassword.value
                    ) {

                        confirmPassword.setCustomValidity(
                            "Passwords do not match"
                        );

                    } else {

                        confirmPassword.setCustomValidity(
                            ""
                        );

                    }

                }
            );

        }


        // Automatically hide flash messages
        setTimeout(
            function () {

                const messages =
                    document.querySelectorAll(
                        ".flash"
                    );

                messages.forEach(
                    function (message) {

                        message.style.opacity = "0";

                        setTimeout(
                            function () {
                                message.remove();
                            },
                            500
                        );

                    }
                );

            },
            5000
        );

    }
);




function changePerPage(value) {

    const url = new URL(window.location.href);

    url.searchParams.set("per_page", value);

    // Reset to page 1 when changing page size
    url.searchParams.set("page", 1);

    window.location.href = url.toString();
}