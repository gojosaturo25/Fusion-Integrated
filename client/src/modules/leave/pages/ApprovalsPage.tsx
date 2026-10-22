import { useState } from "react";
import { Button, Card, Container, Group, TextInput } from "@mantine/core";
import { notifications } from "@mantine/notifications";

import { errorMessage } from "../../../lib/http";
import { DataTable } from "../../../ui/components/DataTable";
import { ErrorState } from "../../../ui/components/ErrorState";
import { PageHeader } from "../../../ui/components/PageHeader";
import { CATEGORY_LABELS, useDecide, useInbox, type Decision, type LeaveApplication } from "../api";

export default function ApprovalsPage() {
  const { data, isPending, error } = useInbox();
  const [remark, setRemark] = useState("");

  if (error) return <Container size="xl"><ErrorState error={error} /></Container>;

  function handleDecision(id: number, decision: Decision, remarkValue: string) {
    useDecide.mutate({ id, decision, remark: remarkValue }, {
      onSuccess: () => {
        notifications.show({
          color: "green",
          title: "Success",
          message: `Decision recorded for application ${id}.`,
        });
        setRemark("");
      },
      onError: (e) => {
        notifications.show({
          color: "red",
          title: "Error",
          message: errorMessage(e),
        });
      },
    });
  }

  const actionsFor = (app: LeaveApplication): { label: string; decision: Decision; color: string }[] => {
    switch (app.stage) {
      case "unit_head":
        if (app.category === "CL" || app.category === "RH") {
          return [
            { label: "Approve", decision: "approve", color: "blue" },
            { label: "Reject", decision: "reject", color: "red" },
          ];
        }
        return [
          { label: "Recommend", decision: "recommended", color: "orange" },
          { label: "Not recommended", decision: "not_recommended", color: "gray" },
        ];
      case "establishment":
        return [{ label: "Verify", decision: "verify", color: "indigo" }];
      case "sanction":
        return [
          { label: "Approve", decision: "approve", color: "blue" },
          { label: "Reject", decision: "reject", color: "red" },
        ];
      default:
        return [];
    }
  };

  const columns = [
    { key: "applicant", header: "Applicant" },
    { key: "category", header: "Category" },
    { key: "start_date", header: "Dates" },
    { key: "days", header: "Days" },
    { key: "purpose", header: "Purpose" },
    { key: "stage", header: "Stage" },
    { key: "unit_head_recommendation", header: "Unit Head recommendation" },
    { key: "actions", header: "Actions" },
  ];

  const rows = data?.results || [];

  return (
    <Container size="xl">
      <PageHeader
        title="Approvals Inbox"
        subtitle="Requests awaiting your decision"
      />
      <TextInput
        label="Remark (optional)"
        value={remark}
        onChange={(e) => setRemark(e.target.value)}
        placeholder="Add a remark for the decision..."
        clearable
      />
      {rows.length === 0 ? (
        <Card padding="lg">
          <Text>No pending approvals</Text>
        </Card>
      ) : (
        <DataTable
          rows={rows}
          columns={columns}
          loading={isPending}
          rowKey={(row: LeaveApplication) => row.id}
          empty={{ title: "No applications found", description: "Check back later for updates." }}
        >
          {(row: LeaveApplication) => {
            const appCategory = row.category;
            const categoryLabel = appCategory === "cancellation" ? `${appCategory.toUpperCase()} (cancellation)` : CATEGORY_LABELS[appCategory];
            const startDate = new Date(row.start_date).toLocaleDateString();
            const endDate = new Date(row.end_date).toLocaleDateString();
            const daysValue = row.days;
            const purpose = row.purpose || "—";
            const stageLabel = row.stage.replace(/_/g, " ");
            const unitHeadRec = row.unit_head_recommendation || "—";

            return (
              <td key="actions">
                {actionsFor(row).map((action) => (
                  <Button
                    key={action.decision}
                    color={action.color}
                    onClick={() => handleDecision(row.id, action.decision, remark)}
                  >
                    {action.label}
                  </Button>
                ))}
              </td>
            );
          }}
        </DataTable>
      )}
    </Container>
  );
}
