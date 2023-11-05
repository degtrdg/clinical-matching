"use client"
import AppOutlet from "@/outlets/AppOutlet"
import {
  ChartPieIcon,
  HomeIcon,
  UsersIcon,
} from '@heroicons/react/24/outline'

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon, current: true },
  { name: 'Patients', href: '/patients', icon: UsersIcon, current: false },
  { name: 'Treatment', href: '/treatment', icon: ChartPieIcon, current: false },
]

export default function Page() {
  return (
    <AppOutlet navigation={navigation}>
        
    </AppOutlet>
  )
}