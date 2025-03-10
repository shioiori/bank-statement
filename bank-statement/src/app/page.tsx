'use client'

import { BillSearch } from "@/components/home/BillSearch";
import { BillTable } from "@/components/home/BillTable";
import { TransactionData } from "@/types/bill";
import { useState } from "react";

export default function Home() {
  const [data, setData] = useState<TransactionData[]>();
  const [filterData, setFilterData] = useState<TransactionData[]>();
  return (
    <div className="container mx-auto p-4">
      <BillSearch/>
      <BillTable data={filterData}/>
    </div>
  );
}
