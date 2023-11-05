"use server"
import prisma from "./prisma";
import { Patient, Response } from "@/types";

const userAlreadyExists = 409;

export async function getPatients(): Promise<Response> {
    try {
        const patients: Patient[] = await prisma.patient.findMany();

        return { status: 200, patients }
    } catch (err) {
        return { status: 500, patients: [] }
    }
}

export async function getPatient(slug: string): Promise<Response> {
    try {
        const patient: Patient | null = await prisma.patient.findUnique({ where: { slug } });
        console.log(patient);

        if (patient) {
            return { status: 200, patient }
        } else {
            return { status: 404, patient: null }
        }
    } catch (err) {
        return { status: 500, patient: null }
    }
}

export async function createPatient(patientData: Patient): Promise<Response> {
    try {
        const patient: any = (await getPatient(patientData.slug)).patient;

        if (!patient) {
            const data: any = { 
                ...patientData,
            }
            const res = await prisma.patient.create({ data: data });

            return { status: 200 }
        } else {
            return { status: userAlreadyExists };
        }
    } catch (err) {
        console.log(err)
        return { status: 500 }
    }
}

export async function addDiagnosis(slug: string, diagnosis: string): Promise<Response> {
    try {
        const user: Patient | undefined | null = (await getPatient(slug)).patient;

        if (user) {
            await prisma.patient.update({
                where: { slug },
                data: { diagnosis, status: "Diagnosed" }
            })

            return { status: 200 }
        } else {
            return { status: 404 }
        }
    } catch (err) {
        return { status: 500 }
    }
}

export async function addTreatement(slug: string, treatment: string): Promise<Response> {
    try {
        const user: Patient | undefined | null = (await getPatient(slug)).patient;

        if (user) {
            await prisma.patient.update({
                where: { slug },
                data: { treatment }
            })

            return { status: 200 }
        } else {
            return { status: 404 }
        }
    } catch (err) {
        return { status: 500 }
    }
}