"use client"
import { useState } from "react";
import { redirect } from "next/navigation";
import AppOutlet from "@/outlets/AppOutlet"
import {
    ChartPieIcon,
    HomeIcon,
    UsersIcon,
} from '@heroicons/react/24/outline';
import { Patient } from "@/types";
import { createPatient } from "@/services/database";

const navigation = [
    { name: 'Dashboard', href: '/', icon: HomeIcon, current: false },
    { name: 'Patients', href: '/patients', icon: UsersIcon, current: true },
    { name: 'Treatment', href: '/treatment', icon: ChartPieIcon, current: false },
]

function getSlug(name: string): string {
    const slug = name.toLowerCase().replace(/ /g, "-");
    return slug;
}

export default function Page() {
    const [isRedirect, setIsRedirect] = useState<boolean>(false);

    async function onSubmit(e: any) {
        e.preventDefault();

        const form = e.currentTarget;
        const fullName = `${form['first-name'].value} ${form['last-name'].value}`;
        const patient: Patient = {
            slug: getSlug(fullName),
            name: fullName,
            email: form['email'].value,
            phone: form['phone'].value,
            status: form['country'].value,
            dob: form['dob'].value,
            complaint: form['complaint'].value,
            imageUrl: form['image-url'].value,
        }

        const res: any = await createPatient(patient);
        
        setIsRedirect(true);
    }

    return (
        <AppOutlet navigation={navigation}>
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div className="pb-6 mb-6 border-b-2 border-gray-200">
                    <h2 className="mt-2 text-2xl font-bold leading-7 sm:text-3xl sm:tracking-tight">
                        Add Patient
                    </h2>
                </div>
                <form onSubmit={onSubmit} className="max-w-3xl">
                    <div className="space-y-12">
                        <div className="border-b border-gray-900/10 pb-12">
                            <h2 className="text-base font-semibold leading-7 text-gray-900">Personal Information</h2>
                            <p className="mt-1 text-sm leading-6 text-gray-600">
                                Enter the patient's personal information.
                            </p>

                            <div className="mt-6 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                                <div className="sm:col-span-3">
                                    <label htmlFor="first-name" className="block text-sm font-medium leading-6 text-gray-900">
                                        First name
                                    </label>
                                    <div className="mt-2">
                                        <input
                                            type="text"
                                            name="first-name"
                                            id="first-name"
                                            autoComplete="given-name"
                                            required
                                            className="block px-3 w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                        />
                                    </div>
                                </div>

                                <div className="sm:col-span-3">
                                    <label htmlFor="last-name" className="block text-sm font-medium leading-6 text-gray-900">
                                        Last name
                                    </label>
                                    <div className="mt-2">
                                        <input
                                            type="text"
                                            name="last-name"
                                            id="last-name"
                                            autoComplete="family-name"
                                            required
                                            className="block px-3 w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                        />
                                    </div>
                                </div>

                                <div className="sm:col-span-3">
                                    <label htmlFor="email" className="block text-sm font-medium leading-6 text-gray-900">
                                        Email address
                                    </label>
                                    <div className="mt-2">
                                        <input
                                            id="email"
                                            name="email"
                                            type="email"
                                            autoComplete="email"
                                            required
                                            className="block w-full px-3 rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                        />
                                    </div>
                                </div>

                                <div className="sm:col-span-3">
                                    <label htmlFor="phone" className="block text-sm font-medium leading-6 text-gray-900">
                                        Phone Number
                                    </label>
                                    <div className="mt-2">
                                        <input
                                            id="phone"
                                            name="phone"
                                            type="tel"
                                            autoComplete="tel"
                                            required
                                            className="block w-full px-3 rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                        />
                                    </div>
                                </div>

                                <div className="sm:col-span-3">
                                    <label htmlFor="country" className="block text-sm font-medium leading-6 text-gray-900">
                                        Status
                                    </label>
                                    <div className="mt-2">
                                        <select
                                            id="country"
                                            name="country"
                                            autoComplete="country-name"
                                            required
                                            className="block w-full rounded-md border-0 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:max-w-xs sm:text-sm sm:leading-6"
                                        >
                                            <option>Undiagnosed</option>
                                            <option>Diagnosed</option>
                                            <option>Recovered</option>
                                            <option>Deceased</option>
                                        </select>
                                    </div>
                                </div>

                                <div className="sm:col-span-3">
                                    <label htmlFor="dob" className="block text-sm font-medium leading-6 text-gray-900">
                                        Date of Birth
                                    </label>
                                    <div className="mt-2">
                                        <input
                                            type="date"
                                            name="dob"
                                            id="dob"
                                            required
                                            className="block w-full rounded-md border-0 px-3 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                        />
                                    </div>
                                </div>

                                <div className="sm:col-span-full">
                                    <label htmlFor="complaint" className="block text-sm font-medium leading-6 text-gray-900">
                                        Primary Complaint
                                    </label>
                                    <div className="mt-2">
                                        <input
                                            type="text"
                                            name="complaint"
                                            id="complaint"
                                            required
                                            className="block w-full rounded-md border-0 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                        />
                                    </div>
                                </div>

                                <div className="sm:col-span-full">
                                    <label htmlFor="image-url" className="block text-sm font-medium leading-6 text-gray-900">
                                        Image URL
                                    </label>
                                    <div className="mt-2">
                                        <input
                                            type="text"
                                            name="image-url"
                                            id="image-url"
                                            required
                                            className="block w-full rounded-md border-0 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="mt-6 flex items-center justify-end gap-x-6">
                        <a href="/patients">
                            <button type="button" className="text-sm font-semibold leading-6 text-gray-900">
                                Cancel
                            </button>
                        </a>
                        <button
                            type="submit"
                            className="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                        >
                            Create Patient
                        </button>
                    </div>
                </form>
            </div>
            {isRedirect && redirect("/patients")}
        </AppOutlet>
    )
}