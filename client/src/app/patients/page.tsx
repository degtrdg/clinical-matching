"use client"
import { useState, useEffect } from "react";
import AppOutlet from "@/outlets/AppOutlet"
import {
    ChartPieIcon,
    HomeIcon,
    UsersIcon,
    PlusIcon
} from '@heroicons/react/24/outline';
import PatientList from "@/components/PatientList";
import { defaultPatients } from "@/config";
import { Patient } from "@/types";
import { getPatients } from "@/services/database";

const navigation = [
    { name: 'Dashboard', href: '/', icon: HomeIcon, current: false },
    { name: 'Patients', href: '/patients', icon: UsersIcon, current: true },
    { name: 'Treatment', href: '/treatment', icon: ChartPieIcon, current: false },
]

async function getPatientsData() {
    const patients: Patient[] | undefined  = (await getPatients()).patients;

    if (!patients) return [];
    return patients
}

export default function Page() {
    const [patients, setPatients] = useState<Patient[]>([])

    useEffect(() => {
        getPatientsData().then((patientsData) => {
            setPatients(patientsData);
        });
    }, []);


    return (
        <AppOutlet navigation={navigation}>
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <div className="pb-6 mb-6 border-b-2 border-gray-200">
                    <h2 className="mt-2 text-2xl font-bold leading-7 sm:text-3xl sm:tracking-tight">
                        Patients
                    </h2>
                </div>
                <div>
                    <PatientList patients={patients} />
                </div>
                <div className="fixed bottom-4 right-4 px-4 sm:px-6 lg:px-8">
                    <a href="/patients/add">
                        <button
                            type="button"
                            className="rounded-full bg-indigo-600 p-3 text-white shadow-lg hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                            aria-label="Add new item"
                        >
                            <PlusIcon className="h-6 w-6" aria-hidden="true" />
                        </button>
                    </a>
                </div>
            </div>
        </AppOutlet>
    )
}