#!/usr/bin/env python3
"""
Validate deployment plan structure and dependencies
"""
import yaml
import sys
import os
from datetime import datetime

def validate_deployment_plan(plan_file):
    """Validate a deployment plan file for structural integrity and requirements"""
    print(f"🔍 Validating deployment plan: {plan_file}")
    
    try:
        with open(plan_file, 'r') as f:
            plan = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"❌ Plan file not found: {plan_file}")
        return False
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error: {e}")
        return False
    
    # Required top-level sections
    required_sections = [
        'metadata', 'description', 'environment', 
        'deployment_steps', 'rollback_plan'
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in plan:
            missing_sections.append(section)
    
    if missing_sections:
        print(f"❌ Missing required sections: {', '.join(missing_sections)}")
        return False
    
    # Validate metadata section
    metadata = plan.get('metadata', {})
    required_metadata = ['name', 'version', 'created_date', 'status']
    missing_metadata = [field for field in required_metadata if field not in metadata]
    
    if missing_metadata:
        print(f"❌ Missing metadata fields: {', '.join(missing_metadata)}")
        return False
    
    # Validate deployment steps
    steps = plan.get('deployment_steps', [])
    if not isinstance(steps, list) or len(steps) == 0:
        print("❌ deployment_steps must be a non-empty list")
        return False
    
    step_names = set()
    for i, step in enumerate(steps):
        if not isinstance(step, dict):
            print(f"❌ Step {i+1} must be a dictionary")
            return False
        
        required_step_fields = ['name', 'assigned_to', 'description', 'estimated_duration']
        missing_step_fields = [field for field in required_step_fields if field not in step]
        
        if missing_step_fields:
            print(f"❌ Step {i+1} missing fields: {', '.join(missing_step_fields)}")
            return False
        
        step_name = step.get('name')
        if step_name in step_names:
            print(f"❌ Duplicate step name: {step_name}")
            return False
        step_names.add(step_name)
        
        # Validate assigned_to is one of the valid Claude instances
        assigned_to = step.get('assigned_to')
        if assigned_to not in ['CDTZ', 'CCN', 'CCW']:
            print(f"❌ Step '{step_name}' assigned to invalid instance: {assigned_to}")
            return False
    
    # Validate rollback plan
    rollback = plan.get('rollback_plan', {})
    if 'trigger_conditions' not in rollback or 'rollback_steps' not in rollback:
        print("❌ rollback_plan must include trigger_conditions and rollback_steps")
        return False
    
    # Validate environment section
    environment = plan.get('environment', {})
    if 'target_machines' not in environment:
        print("❌ environment section must include target_machines")
        return False
    
    # Check for reasonable resource requirements
    machines = environment.get('target_machines', [])
    for machine in machines:
        if 'resources_required' in machine:
            resources = machine['resources_required']
            if 'memory' in resources:
                memory = resources['memory']
                if not memory.endswith('GB') and not memory.endswith('MB'):
                    print(f"⚠️  Warning: Memory specification '{memory}' should include GB or MB")
    
    print(f"✅ {plan_file} is structurally valid")
    
    # Additional validations and warnings
    warnings = []
    
    # Check for estimated duration format
    total_duration = 0
    for step in steps:
        duration_str = step.get('estimated_duration', '0 minutes')
        try:
            # Simple parsing for "X minutes" format
            if 'minute' in duration_str:
                duration = int(duration_str.split()[0])
                total_duration += duration
        except (ValueError, IndexError):
            warnings.append(f"Step '{step['name']}' has non-standard duration format: {duration_str}")
    
    if total_duration > 120:  # More than 2 hours
        warnings.append(f"Total estimated duration ({total_duration} minutes) is quite long - consider breaking into smaller deployments")
    
    # Check for external integrations
    external_integrations = plan.get('external_integrations', {})
    if external_integrations:
        print(f"ℹ️  External integrations required: {', '.join(external_integrations.keys())}")
    
    # Display warnings
    for warning in warnings:
        print(f"⚠️  Warning: {warning}")
    
    # Summary
    print(f"📊 Plan summary:")
    print(f"   • {len(steps)} deployment steps")
    print(f"   • {len(machines)} target machines")
    print(f"   • {total_duration} minutes estimated duration")
    print(f"   • {len(external_integrations)} external integrations")
    
    return True

def validate_dependencies(plan_file):
    """Check if plan dependencies are satisfied"""
    try:
        with open(plan_file, 'r') as f:
            plan = yaml.safe_load(f)
    except:
        return False
    
    dependencies = plan.get('prerequisites', {}).get('dependencies', [])
    if not dependencies:
        print("ℹ️  No dependencies specified")
        return True
    
    print(f"🔗 Checking {len(dependencies)} dependencies...")
    
    # Check if dependency deployment plans exist and are completed
    for dep in dependencies:
        dep_name = dep.get('deployment')
        if not dep_name:
            continue
        
        # Look for the dependency in completed deployments
        completed_dir = os.path.join(os.path.dirname(plan_file), '..', 'completed')
        if os.path.exists(completed_dir):
            completed_files = [f for f in os.listdir(completed_dir) if f.endswith('.yml')]
            dep_found = any(dep_name in f for f in completed_files)
            if dep_found:
                print(f"   ✅ Dependency '{dep_name}' found in completed deployments")
            else:
                print(f"   ⚠️  Dependency '{dep_name}' not found in completed deployments")
        else:
            print(f"   ⚠️  Completed deployments directory not found")
    
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: validate-deployment-plan.py <plan-file>")
        print("       validate-deployment-plan.py --help")
        sys.exit(1)
    
    if sys.argv[1] == '--help':
        print("""
Deployment Plan Validator

This tool validates DoggPack deployment plans for structural integrity,
required fields, and logical consistency.

Validation checks:
• Required sections and fields
• Step name uniqueness
• Valid Claude instance assignments
• Resource specification format
• Dependency consistency
• Duration estimates

Usage:
    python validate-deployment-plan.py path/to/plan.yml
        """)
        sys.exit(0)
    
    plan_file = sys.argv[1]
    
    if not os.path.exists(plan_file):
        print(f"❌ Plan file not found: {plan_file}")
        sys.exit(1)
    
    # Run validations
    structure_valid = validate_deployment_plan(plan_file)
    dependencies_valid = validate_dependencies(plan_file)
    
    if structure_valid and dependencies_valid:
        print(f"\n🎉 Deployment plan validation successful!")
        sys.exit(0)
    else:
        print(f"\n❌ Deployment plan validation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
