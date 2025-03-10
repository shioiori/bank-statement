import { sampleData } from "@/samples/bill"
import { TransactionData } from "@/types/bill"
import { Table } from "antd"
import dayjs from "dayjs"

interface IProps{
  data?: TransactionData[]
}

export const BillTable = (props: IProps) => {
  const columns = [
    {
      title: "Ngày",
      dataIndex: "date",
      key: "date",
      sorter: (a, b) => dayjs(a.date).unix() - dayjs(b.date).unix(),
    },
    {
      title: "Số tiền",
      dataIndex: "amount",
      key: "amount",
      render: (amount: number) => `${amount.toLocaleString()} VND`,
    },
    {
      title: "Nội dung giao dịch",
      dataIndex: "description",
      key: "description",
    },
    {
      title: "Ngân hàng",
      dataIndex: "bank",
      key: "bank",
    },
  ]

  return (
    <Table 
      columns={columns}
      dataSource={props.data ?? sampleData}/>
  )
}