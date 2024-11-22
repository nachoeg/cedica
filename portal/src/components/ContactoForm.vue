<template>
    <div class="max-w-md mx-auto p-6 bg-white/65 rounded-lg shadow-md backdrop-blur-md dark:bg-neutral-800/65">
        <h2 class="text-2xl font-bold mb-4 text-neutral-900 dark:text-white">Contacto</h2>
        <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- Título -->
        <div>
            <label for="titulo" class="block text-sm font-medium text-neutral-800 dark:text-neutral-300">
            Título
            </label>
            <input
            type="text"
            id="titulo"
            v-model="formData.titulo"
            required
            class="mt-1 block w-full rounded-md border-neutral-300 bg-white text-neutral-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-neutral-700 dark:border-neutral-600 dark:text-neutral-300"
            />
        </div>
        <!-- Email -->
        <div>
            <label for="email" class="block text-sm font-medium text-neutral-800 dark:text-neutral-300">
            Email
            </label>
            <input
            type="email"
            id="email"
            v-model="formData.email"
            required
            class="mt-1 block w-full rounded-md border-neutral-300 bg-white text-neutral-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-neutral-700 dark:border-neutral-600 dark:text-neutral-300"
            />
        </div>
        <!-- Mensaje -->
        <div>
            <label for="mensaje" class="block text-sm font-medium text-neutral-800 dark:text-neutral-300">
            Mensaje
            </label>
            <textarea
            id="mensaje"
            v-model="formData.mensaje"
            required
            rows="4"
            class="mt-1 block w-full rounded-md border-neutral-300 bg-white text-neutral-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-neutral-700 dark:border-neutral-600 dark:text-neutral-300"
            ></textarea>
        </div>
        <!-- reCAPTCHA -->
        <div class="mt-4">
            <div
            id="recaptcha"
            class="g-recaptcha"
            data-sitekey="6Ldhj4YqAAAAAIUOpoUYXTzLUlSmKCNIyVppBnPY"
            data-callback="onCaptchaVerified"
        ></div>
        </div>
        <!-- Botón Enviar -->
        <button
            type="submit"
            :disabled="!captchaToken"
            class="w-full px-4 py-2 bg-indigo-600 text-white rounded-md shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 dark:focus:ring-offset-neutral-800"
        >
            Enviar
        </button>
        </form>
        <p v-if="mensaje" class="mt-4 text-center text-green-600 dark:text-green-400">{{ mensaje }}</p>
    </div>
</template>

<script>
    export default {
    data() {
        return {
        formData: {
            titulo: "",
            email: "",
            mensaje: "",
        },
        mensaje: null,
        captchaToken: null, 
        };
    },
    methods: {
        async handleSubmit() {
        if (!this.captchaToken) {
            this.mensaje = "Por favor, completa el captcha.";
            return;
        }
        try {
            const response = await fetch("https://admin-grupo17.proyecto2024.linti.unlp.edu.ar/api/message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
                body: JSON.stringify({ ...this.formData, captchaToken: this.captchaToken }),
            });
            if (response.ok) {
                this.mensaje = "Mensaje enviado con éxito.";
                this.formData = { titulo: "", email: "", mensaje: "" };
                this.captchaToken = null; 
                grecaptcha.reset();
            } else {
            const error = await response.json();
                this.mensaje = `Error: ${error.message}`;
            }
        } catch (err) {
            this.mensaje = "Error de conexión con la API.";
        }
        },
        onCaptchaVerified(token) {
        this.captchaToken = token;
        }
    },
    mounted() {
    this.$nextTick(() => {
        grecaptcha.render('recaptcha', {
        sitekey: '6Ldhj4YqAAAAAIUOpoUYXTzLUlSmKCNIyVppBnPY',
        callback: this.onCaptchaVerified,
        });
    });
    },
};
</script>  