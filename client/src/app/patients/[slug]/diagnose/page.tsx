
"use client"
import AppOutlet from "@/outlets/AppOutlet"
import { useState } from "react";
import {
    ChartPieIcon,
    HomeIcon,
    UsersIcon,
    ArrowUpTrayIcon
} from '@heroicons/react/24/outline';
import { defaultPatients } from "@/config";
import { Patient } from "@/types";
import Page404 from "@/components/Page404";

const navigation = [
    { name: 'Dashboard', href: '/', icon: HomeIcon, current: false },
    { name: 'Patients', href: '/patients', icon: UsersIcon, current: true },
    { name: 'Treatment', href: '/treatment', icon: ChartPieIcon, current: false },
]

export default function Page({ params }: { params: { slug: string } }) {
    const [file, setFile] = useState<any>(null);
    const patient: Patient | undefined = defaultPatients.find((patient) => patient.slug === params.slug);

    function onSubmit(e: any) {
        e.preventDefault();

        const form = e.target;
        // const file = form.files[0];

        console.log(file);
    }

    function onAttach(e: any) {
        e.preventDefault();

        const form = e.target;
        const file = form.files[0];

        setFile(file);
    }

    return (
        patient ? (
            <AppOutlet navigation={navigation}>
                <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
                    <div className="pb-6 mb-6 border-b-2 border-gray-200">
                        <h2 className="mt-2 text-2xl font-bold leading-7 sm:text-3xl sm:tracking-tight">
                            Diagnose: {patient.name}
                        </h2>
                    </div>
                    <div className="flex flex-col gap-y-6">
                        <div>
                            <h3 className="mt-2 text-lg font-bold leading-7 sm:text-xl sm:tracking-tight">
                                Analyze Biopsy
                            </h3>
                        </div>
                        <form onSubmit={onSubmit} className="flex flex-col gap-y-6 max-w-lg">
                            <label
                                className="relative block w-1/2 rounded-lg border-2 border-dashed border-gray-300 p-6 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 cursor-pointer"
                            >
                                <input
                                    id="csv-file"
                                    type="file"
                                    className="sr-only"
                                    accept=".csv"
                                    onChange={onAttach}
                                />
                                <ArrowUpTrayIcon className="mx-auto h-6 w-6 text-gray-900" aria-hidden="true" />


                                {
                                    file ? (
                                        <p className="text-sm text-gray-600 mt-2">
                                            Uploaded File: {file.name} ({Math.round((file.size || 0) / 1024)} KB)
                                        </p>
                                    ) : (
                                        <span className="mt-2 block text-sm font-semibold text-gray-900">Upload CSV File</span>
                                    )
                                }
                            </label>

                            <div className="">
                                <button
                                    type="submit"
                                    className="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                >
                                    Analyze Results
                                </button>
                            </div>
                        </form>

                    </div>
                </div>
            </AppOutlet>
        ) : (
            <Page404 />
        )
    )
};