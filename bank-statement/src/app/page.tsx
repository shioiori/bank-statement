'use client'

import { BillSearch } from "@/components/home/BillSearch";
import { BillTable } from "@/components/home/BillTable";
import { TransactionData } from "@/types/bill";
import { useEffect, useState } from "react";

export default function Home() {
  const [data, setData] = useState<TransactionData[]>();
  const [filterData, setFilterData] = useState<TransactionData[]>();
  
  useEffect(() => {
    const fetchData: TransactionData[] = [];
    setData(fetchData);
    setFilterData(fetchData);
  }, [])
  
  return (
    <div className="container mx-auto p-4">
      <BillSearch/>
      <BillTable data={data ?? filterData}/>
    </div>
  );
}
