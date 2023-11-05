"use client"
import { useEffect, useState } from "react";
import AppOutlet from "@/outlets/AppOutlet"
import {
    ChartPieIcon,
    HomeIcon,
    UsersIcon,
} from '@heroicons/react/24/outline';
import { CheckIcon, HandThumbUpIcon, UserIcon, PaperClipIcon } from '@heroicons/react/20/solid'
import { Patient } from "@/types";
import { getPatient } from "@/services/database";
import Page404 from "@/components/Page404";

function classNames(...classes: any) {
    return classes.filter(Boolean).join(' ')
}

const navigation = [
    { name: 'Dashboard', href: '/', icon: HomeIcon, current: false },
    { name: 'Patients', href: '/patients', icon: UsersIcon, current: true },
    { name: 'Treatment', href: '/treatment', icon: ChartPieIcon, current: false },
]

const timeline = [
    {
        id: 1,
        content: 'Applied to',
        target: 'Front End Developer',
        href: '#',
        date: 'Sep 20',
        datetime: '2020-09-20',
        icon: UserIcon,
        iconBackground: 'bg-gray-400',
    },
    {
        id: 2,
        content: 'Advanced to phone screening by',
        target: 'Bethany Blake',
        href: '#',
        date: 'Sep 22',
        datetime: '2020-09-22',
        icon: HandThumbUpIcon,
        iconBackground: 'bg-blue-500',
    },
    {
        id: 3,
        content: 'Completed phone screening with',
        target: 'Martha Gardner',
        href: '#',
        date: 'Sep 28',
        datetime: '2020-09-28',
        icon: CheckIcon,
        iconBackground: 'bg-green-500',
    },
    {
        id: 4,
        content: 'Advanced to interview by',
        target: 'Bethany Blake',
        href: '#',
        date: 'Sep 30',
        datetime: '2020-09-30',
        icon: HandThumbUpIcon,
        iconBackground: 'bg-blue-500',
    },
    {
        id: 5,
        content: 'Completed interview with',
        target: 'Katherine Snyder',
        href: '#',
        date: 'Oct 4',
        datetime: '2020-10-04',
        icon: CheckIcon,
        iconBackground: 'bg-green-500',
    },
]

export default function Page({ params }: { params: { slug: string } }) {
    const [patient, setPatient] = useState<Patient | undefined>(undefined);

    async function getPatientData() {
        const patientData: Patient | undefined  = (await getPatient(params.slug)).patient;
    
        if (!patientData) return undefined;
        return patientData
    }

    useEffect(() => {
        getPatientData().then((patientData) => {
            setPatient(patientData);
        });
    }, []);

    return (
        patient ? (
            <AppOutlet navigation={navigation}>
                <div>
                    <div className="px-4 sm:px-0">
                        <div>

                        </div>
                        <div>
                            <h3 className="text-base font-semibold leading-7 text-gray-900">Patient Information</h3>
                            <p className="mt-1 max-w-2xl text-sm leading-6 text-gray-500">Personal details and application.</p>
                        </div>
                    </div>
                    <div className="mt-6 border-t border-gray-100">
                        <dl className="divide-y divide-gray-100">
                            <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
                                <dt className="text-sm font-medium leading-6 text-gray-900">Full name</dt>
                                <dd className="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{patient.name}</dd>
                            </div>
                            <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
                                <dt className="text-sm font-medium leading-6 text-gray-900">Primary Complaint</dt>
                                <dd className="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{patient.complaint}</dd>
                            </div>
                            <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
                                <dt className="text-sm font-medium leading-6 text-gray-900">Status</dt>
                                <dd className="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{patient.status}</dd>
                            </div>
                            <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
                                <dt className="text-sm font-medium leading-6 text-gray-900">Email address</dt>
                                <dd className="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{patient.email}</dd>
                            </div>
                            <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
                                <dt className="text-sm font-medium leading-6 text-gray-900">Phone</dt>
                                <dd className="mt-1 text-sm leading-6 text-gray-700 sm:col-span-2 sm:mt-0">{patient.phone}</dd>
                            </div>
                            <div className="px-4 py-6 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-0">
                                <dt className="text-sm font-medium leading-6 text-gray-900">Attachments</dt>
                                <dd className="mt-2 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
                                    <ul role="list" className="divide-y divide-gray-100 rounded-md border border-gray-200">
                                        <li className="flex items-center justify-between py-4 pl-4 pr-5 text-sm leading-6">
                                            <div className="flex w-0 flex-1 items-center">
                                                <PaperClipIcon className="h-5 w-5 flex-shrink-0 text-gray-400" aria-hidden="true" />
                                                <div className="ml-4 flex min-w-0 flex-1 gap-2">
                                                    <span className="truncate font-medium">Cat-scan-results.pdf</span>
                                                    <span className="flex-shrink-0 text-gray-400">2.4mb</span>
                                                </div>
                                            </div>
                                            <div className="ml-4 flex-shrink-0">
                                                <a href="#" className="font-medium text-indigo-600 hover:text-indigo-500">
                                                    Download
                                                </a>
                                            </div>
                                        </li>
                                        <li className="flex items-center justify-between py-4 pl-4 pr-5 text-sm leading-6">
                                            <div className="flex w-0 flex-1 items-center">
                                                <PaperClipIcon className="h-5 w-5 flex-shrink-0 text-gray-400" aria-hidden="true" />
                                                <div className="ml-4 flex min-w-0 flex-1 gap-2">
                                                    <span className="truncate font-medium">Blood-lab-work.pdf</span>
                                                    <span className="flex-shrink-0 text-gray-400">4.5mb</span>
                                                </div>
                                            </div>
                                            <div className="ml-4 flex-shrink-0">
                                                <a href="#" className="font-medium text-indigo-600 hover:text-indigo-500">
                                                    Download
                                                </a>
                                            </div>
                                        </li>
                                    </ul>
                                </dd>
                            </div>
                            {
                                (patient.status == "Undiagnosed") && (
                                    <div className="flex justify-center px-4 py-6 sm:px-0">
                                    <a
                                        href={`/patients/${params.slug}/diagnose`}
                                        className="text-center rounded-md w-full max-w-sm bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                    >
                                        Diagnose
                                    </a>
                                </div>
                                )
                            }
                        </dl>
                    </div>
                </div>

            </AppOutlet>
        ) : (
            <Page404 />
        )
    );
}
