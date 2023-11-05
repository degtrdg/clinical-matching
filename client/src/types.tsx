export interface Response {
    status: number;
    patients?: Patient[];
    patient?: any | null;
    error?: any;
}

export interface Patient {
    slug: string;
    name: string;
    email: string;
    phone: string;
    status: string;
    dob: string;
    complaint: string;
    imageUrl: string;
    diagnosis?: string;
    treatment?: string;
}