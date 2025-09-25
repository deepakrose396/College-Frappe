import { userResource } from "@/data/user"
import { createRouter, createWebHistory } from "vue-router"
import { session } from "./data/session"



const routes = [
	{
		path: "/",
		name: "Home",
		component: () => import("@/pages/Home.vue"),
	},
	{
		name: "Login",
		path: "/account/login",
		component: () => import("@/pages/Login.vue"),
	},

	{
		name: "Navbar",
		path: "/navbar",
		component: () => import("@/pages/Navbar.vue"),
	},
	{
		path: "/application",
		name: "ApplicationForm",
		component: () => import("@/components/ApplicationForm.vue"),
		meta: { requiresAuth: false }   // 👈 add this
	},
	{
		path: "/set-password",
		name: "SetPassword",
		component: () => import("@/components/SetPassword.vue"),
		meta: { requiresAuth: false }
	},
	{
		path: "/my-profile",
		name: "ApplicantProfile",
		component: () => import("@/components/ApplicantProfile.vue"),
		meta: { requiresAuth: true }
	}

]

const router = createRouter({
	history: createWebHistory("/frontend"),
	routes,
})

const publicPages = ["Login", "Navbar","ApplicationForm", "SetPassword"]; // 👈 add your public routes here

router.beforeEach(async (to, from, next) => {
	let isLoggedIn = session.isLoggedIn
	try {
		await userResource.promise
	} catch (error) {
		isLoggedIn = false
	}

	if (to.name === "Login" && isLoggedIn) {
		next({ name: "ApplicantProfile" })
	} else if (!publicPages.includes(to.name) && !isLoggedIn) {
		next({ name: "Login" })  // 👈 only protect private pages
	} else {
		next()
	}
})


export default router
