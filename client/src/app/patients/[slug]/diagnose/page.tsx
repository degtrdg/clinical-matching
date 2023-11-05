
"use client"
import AppOutlet from "@/outlets/AppOutlet"
import { useState, useEffect } from "react";
import {
    ChartPieIcon,
    HomeIcon,
    UsersIcon,
    ArrowUpTrayIcon,
    CheckCircleIcon,
    AcademicCapIcon,
    BanknotesIcon,
    CheckBadgeIcon,
    ClockIcon,
    ReceiptRefundIcon,
} from '@heroicons/react/24/outline';
import { Patient } from "@/types";
import HorizontalBarGraph from "@/components/BarGraph";
import Page404 from "@/components/Page404";
import { addDiagnosis, getPatient } from "@/services/database";
import { patientTrialRequestData, cachedPatientTrialResponse } from "@/config";

function classNames(...classes: any) {
    return classes.filter(Boolean).join(' ')
}

const navigation = [
    { name: 'Dashboard', href: '/', icon: HomeIcon, current: false },
    { name: 'Patients', href: '/patients', icon: UsersIcon, current: true },
    { name: 'Treatment', href: '/treatment', icon: ChartPieIcon, current: false },
]

const stringLimit = 350;

function limitString(str: string, limit: number = stringLimit) {
    if (str.length > limit) {
        return str.substring(0, limit) + "...";
    }
    return str;
}

function getNCTLink(nct: string) {
    return `https://classic.clinicaltrials.gov/ct2/show/results/${nct}?view=results`
}

export default function Page({ params }: { params: { slug: string } }) {
    const [file, setFile] = useState<any>(null);
    const [selectedPlan, setSelectedPlan] = useState<string>('OV');
    const [diagnosed, setDiagnosed] = useState<boolean>(false);
    const [processing, setProcessing] = useState<boolean>(false);
    const [prediction, setPrediction] = useState<any>(null);
    const [patient, setPatient] = useState<Patient | null>(null);
    const [trials, setTrials] = useState<any[]>([]);

    async function getPatientData() {
        const patients: Patient[] | undefined = (await getPatient(params.slug)).patients;

        if (!patients) return [];
        return patients
    }

    const debugging = true;

    async function getTrialsData(patientData: string) {
        fetch("http://0.0.0.0:8000/get_patient_match_result/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "metadata": {
                    "key1": "value1",
                    "key2": "value2"
                },
                "patient": patientData,
            }),
        })
            .then(response => response.json())
            .then(data => {
                setTrials(data.trials);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    useEffect(() => {
        getPatientData().then((patientData) => {
            setPatient(patientData);
        });
        if (debugging) {
            setTrials(cachedPatientTrialResponse.data.result)
        } else {
            getTrialsData(patientTrialRequestData.patient).then((trialData: any) => {
                setTrials(trialData.data.result);
            });
        }
    }, []);

    async function onSubmit(e: any) {
        e.preventDefault();

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://0.0.0.0:8000/uploadcsv/?file', {
                method: 'POST',
                body: formData,
            });
            if (!response.ok) {
                throw new Error(`Error: ${response.status}`);
            }
            setProcessing(true);
            const data = await response.json();

            setPrediction(data);

            setProcessing(false);
            console.log(data);
        } catch (error) {
            console.error("Failed to upload file:", error);
        }
    }

    function onAttach(e: any) {
        e.preventDefault();

        const form = e.target;
        const file = form.files[0];

        setFile(file);
    }

    const handleSelectionChange = (key: string) => {
        setSelectedPlan(key);
    };

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();

        addDiagnosis(params.slug || "", selectedPlan)
        setDiagnosed(true);
    };

    return (
        patient ? (
            <AppOutlet navigation={navigation}>
                <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
                    <div className="pb-6 mb-6 border-b-2 border-gray-200">
                        <h2 className="mt-2 text-2xl font-bold leading-7 sm:text-3xl sm:tracking-tight">
                            {patient.name}
                        </h2>
                    </div>
                    <div className="flex flex-col gap-y-6">
                        <div>
                            <h3 className="mt-2 text-lg font-bold leading-7 sm:text-xl sm:tracking-tight">
                                {prediction ? "Diagnose Patient" : "Analyze Biopsy"}
                            </h3>
                        </div>
                        {
                            diagnosed ? (
                                <div className="rounded-md bg-green-50 p-4">
                                    <div className="flex">
                                        <div className="flex-shrink-0">
                                            <CheckCircleIcon className="h-5 w-5 text-green-400" aria-hidden="true" />
                                        </div>
                                        <div className="ml-3">
                                            <h3 className="text-sm font-medium text-green-800">Diagnosis Complete</h3>
                                            <div className="mt-2 text-sm text-green-700">
                                                <p>You have diagnosed {patient.name} with {selectedPlan}.</p>
                                            </div>
                                            <div className="mt-4">
                                                <div className="-mx-2 -my-1.5 flex">
                                                    <a href={`/patients/${patient.slug}`}>
                                                        <button
                                                            type="button"
                                                            className="rounded-md bg-green-50 px-2 py-1.5 text-sm font-medium text-green-800 hover:bg-green-100 focus:outline-none focus:ring-2 focus:ring-green-600 focus:ring-offset-2 focus:ring-offset-green-50"
                                                        >
                                                            View Patient
                                                        </button>
                                                    </a>
                                                    <button
                                                        type="button"
                                                        className="ml-3 rounded-md bg-green-50 px-2 py-1.5 text-sm font-medium text-green-800 hover:bg-green-100 focus:outline-none focus:ring-2 focus:ring-green-600 focus:ring-offset-2 focus:ring-offset-green-50"
                                                    >
                                                        Dismiss
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ) : (prediction ? (
                                <div className="container mx-auto">
                                    <form onSubmit={handleSubmit}>
                                        <HorizontalBarGraph data={prediction} selected={selectedPlan} onChange={handleSelectionChange} />
                                        <button
                                            type="submit"
                                            className="mt-6 px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                                        >
                                            Diagnose
                                        </button>
                                    </form>
                                </div>
                            ) : (
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
                                        {
                                            processing ? (
                                                <div>
                                                    <p className="text-sm text-gray-600 mt-2">
                                                        Processing...
                                                    </p>
                                                </div>
                                            ) : (
                                                <button
                                                    type="submit"
                                                    className="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                                >
                                                    Analyze Results
                                                </button>
                                            )
                                        }
                                    </div>
                                </form>
                            ))
                        }
                    </div>
                    <div className="mt-6">
                        <h3 className="mt-2 text-lg font-bold leading-7 sm:text-xl sm:tracking-tight">
                            Related Trials
                        </h3>

                        <div className="divide-y divide-gray-200 overflow-hidden rounded-lg bg-gray-200 shadow sm:grid sm:grid-cols-2 sm:gap-px sm:divide-y-0">
                            {trials.map((trial, trialIdx) => (
                                <div
                                    key={trial.metadata["Brief Title"]}
                                    className={classNames(
                                        trialIdx === 0 ? 'rounded-tl-lg rounded-tr-lg sm:rounded-tr-none' : '',
                                        trialIdx === 1 ? 'sm:rounded-tr-lg' : '',
                                        'group relative bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-500'
                                    )}
                                >
                                    <div className="mt-8">
                                        <h3 className="text-base font-semibold leading-6 text-gray-900">
                                            <a href={getNCTLink(trial.metadata["NCT ID"])} className="focus:outline-none">
                                                {/* Extend touch target to entire panel */}
                                                <span className="absolute inset-0" aria-hidden="true" />
                                                {trial.metadata["Brief Title"]}
                                            </a>
                                        </h3>
                                        <p className="mt-2 text-sm text-gray-500">
                                            {trial.metadata["Brief Summary"]}
                                        </p>
                                    </div>
                                    <div className="mt-8">
                                        <h3 className="text-base font-semibold leading-6 text-gray-900">
                                            <a href={getNCTLink(trial.metadata["NCT ID"])} className="focus:outline-none">
                                                {/* Extend touch target to entire panel */}
                                                <span className="absolute inset-0" aria-hidden="true" />
                                                Match Reasoning
                                            </a>
                                        </h3>
                                        <p className="mt-2 text-sm text-gray-500">
                                            {limitString(trial.patient_match_result["reasoning"])}
                                        </p>
                                    </div>
                                    <span
                                        className="pointer-events-none absolute right-6 top-6 text-gray-300 group-hover:text-gray-400"
                                        aria-hidden="true"
                                    >
                                        <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
                                            <path d="M20 4h1a1 1 0 00-1-1v1zm-1 12a1 1 0 102 0h-2zM8 3a1 1 0 000 2V3zM3.293 19.293a1 1 0 101.414 1.414l-1.414-1.414zM19 4v12h2V4h-2zm1-1H8v2h12V3zm-.707.293l-16 16 1.414 1.414 16-16-1.414-1.414z" />
                                        </svg>
                                    </span>
                                </div>
                            ))}
                        </div>


                    </div>
                </div>
            </AppOutlet>
        ) : (
            <Page404 />
        )
    )
};