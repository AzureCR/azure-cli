# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.help_files import helps
# pylint: disable=line-too-long, too-many-lines

helps['backup'] = """
type: group
short-summary: Manage Azure Backups.
"""

helps['backup container'] = """
type: group
short-summary: Resource which houses items or applications to be protected.
"""

helps['backup container list'] = """
type: command
short-summary: List containers registered to a Recovery services vault.
examples:
  - name: List containers registered to a Recovery services vault. (autogenerated)
    text: az backup container list --resource-group MyResourceGroup --vault-name MyVault
    crafted: true
"""

helps['backup container show'] = """
type: command
short-summary: Show details of a container registered to a Recovery services vault.
"""

helps['backup item'] = """
type: group
short-summary: An item which is already protected or backed up to an Azure Recovery services vault with an associated policy.
"""

helps['backup item list'] = """
type: command
short-summary: List all backed up items within a container.
examples:
  - name: List all backed up items within a container. (autogenerated)
    text: az backup item list --resource-group MyResourceGroup --vault-name MyVault
    crafted: true
"""

helps['backup item set-policy'] = """
type: command
short-summary: Update the policy associated with this item.
"""

helps['backup item show'] = """
type: command
short-summary: Show details of a particular backed up item.
"""

helps['backup job'] = """
type: group
short-summary: Entity which contains details of the job.
"""

helps['backup job list'] = """
type: command
short-summary: List all backup jobs of a Recovery Services vault.
examples:
  - name: List all backup jobs of a Recovery Services vault
    text: az backup job list --resource-group MyResourceGroup --vault-name MyVault
    crafted: true
"""

helps['backup job show'] = """
type: command
short-summary: Show details of a particular job.
examples:
  - name: Show details of a particular job. (autogenerated)
    text: az backup job show --name MyJob --resource-group MyResourceGroup --vault-name MyVault
    crafted: true
"""

helps['backup job stop'] = """
type: command
short-summary: Suspend or terminate a currently running job.
"""

helps['backup job wait'] = """
type: command
short-summary: Wait until either the job completes or the specified timeout value is reached.
"""

helps['backup policy'] = """
type: group
short-summary: A backup policy defines when you want to take a backup and for how long you would retain each backup copy.
"""

helps['backup policy delete'] = """
type: command
short-summary: Before you can delete a Backup protection policy, the policy must not have any associated Backup items. To  associate another policy with a Backup item, use the backup item set-policy command.
"""

helps['backup policy get-default-for-vm'] = """
type: command
short-summary: Get the default policy with default values to backup a VM.
"""

helps['backup policy list'] = """
type: command
short-summary: List all policies for a Recovery services vault.
examples:
  - name: List all policies for a Recovery services vault. (autogenerated)
    text: az backup policy list --resource-group MyResourceGroup --vault-name MyVault
    crafted: true
"""

helps['backup policy list-associated-items'] = """
type: command
short-summary: List all items protected by a backup policy.
"""

helps['backup policy set'] = """
type: command
short-summary: Update the properties of the backup policy.
"""

helps['backup policy show'] = """
type: command
short-summary: Show details of a particular policy.
"""

helps['backup protection'] = """
type: group
short-summary: Manage protection of your items, enable protection or disable it, or take on-demand backups.
"""

helps['backup protection backup-now'] = """
type: command
short-summary: Perform an on-demand backup of a backed up item.
examples:
  - name: Perform an on-demand backup of a backed up item. (autogenerated)
    text: az backup protection backup-now --container-name MyContainer --item-name MyItem --resource-group MyResourceGroup --retain-until 01-02-2018 --vault-name MyVault
    crafted: true
"""

helps['backup protection check-vm'] = """
type: command
short-summary: Find out whether the virtual machine is protected or not. If protected, it returns the recovery services vault ID, otherwise it returns empty.
"""

helps['backup protection disable'] = """
type: command
short-summary: Stop protecting a backed up Azure VM.
"""

helps['backup protection enable-for-vm'] = """
type: command
short-summary: Start protecting a previously unprotected Azure VM as per the specified policy to a Recovery services vault.
examples:
  - name: Start protecting a previously unprotected Azure VM as per the specified policy to a Recovery services vault. (autogenerated)
    text: az backup protection enable-for-vm --policy-name MyPolicy --resource-group MyResourceGroup --vault-name MyVault --vm myVM
    crafted: true
"""

helps['backup recoverypoint'] = """
type: group
short-summary: A snapshot of data at that point-of-time, stored in Recovery Services Vault, from which you can restore information.
"""

helps['backup recoverypoint list'] = """
type: command
short-summary: List all recovery points of a backed up item.
examples:
  - name: List all recovery points of a backed up item. (autogenerated)
    text: az backup recoverypoint list --container-name MyContainer --item-name MyItem --resource-group MyResourceGroup --vault-name MyVault
    crafted: true
"""

helps['backup recoverypoint show'] = """
type: command
short-summary: Shows details of a particular recovery point.
"""

helps['backup restore'] = """
type: group
short-summary: Restore backed up items from recovery points in a Recovery Services vault.
"""

helps['backup restore files'] = """
type: group
short-summary: Gives access to all files of a recovery point.
"""

helps['backup restore files mount-rp'] = """
type: command
short-summary: Download a script which mounts files of a recovery point.
"""

helps['backup restore files unmount-rp'] = """
type: command
short-summary: Close access to the recovery point.
"""

helps['backup restore restore-disks'] = """
type: command
short-summary: Restore disks of the backed VM from the specified recovery point.
examples:
  - name: Restore disks of the backed VM from the specified recovery point. (autogenerated)
    text: az backup restore restore-disks --container-name MyContainer --item-name MyItem --resource-group MyResourceGroup --rp-name MyRp --storage-account mystorageaccount --vault-name MyVault
    crafted: true
"""

helps['backup vault'] = """
type: group
short-summary: Online storage entity in Azure used to hold data such as backup copies, recovery points and backup policies.
"""

helps['backup vault backup-properties'] = """
type: group
short-summary: Properties of the Recovery Services vault.
"""

helps['backup vault backup-properties set'] = """
type: command
short-summary: Sets backup related properties of the Recovery Services vault.
"""

helps['backup vault backup-properties show'] = """
type: command
short-summary: Gets backup related properties of the Recovery Services vault.
"""

helps['backup vault create'] = """
type: command
short-summary: Create a new Recovery Services vault.
examples:
  - name: Create a new Recovery Services vault. (autogenerated)
    text: az backup vault create --location westus2 --name MyRecoveryServicesVault --resource-group MyResourceGroup
    crafted: true
"""

helps['backup vault delete'] = """
type: command
short-summary: Delete an existing Recovery services vault.
"""

helps['backup vault list'] = """
type: command
short-summary: List Recovery service vaults within a subscription.
"""

helps['backup vault show'] = """
type: command
short-summary: Show details of a particular Recovery service vault.
examples:
  - name: Show details of a particular Recovery service vault. (autogenerated)
    text: az backup vault show --name MyRecoveryServicesVault --resource-group MyResourceGroup
    crafted: true
"""
