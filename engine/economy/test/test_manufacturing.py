"""
Unit tests for the manufacturing system.
Tests the core functionality of manufacturing projects and includes comprehensive examples.
"""

import unittest
from economy.manufacture import TManufacture
from economy.manufacturing_project import ManufacturingProject
from economy.manufacturing_manager import ManufacturingManager


class TestManufacturingSystem(unittest.TestCase):
    
    def setUp(self):
        """Set up test data."""
        self.manufacturing_data = {
            'manufacturing': {
                'test_item': {
                    'name': 'Test Item',
                    'category': 'test',
                    'build_time': 5,
                    'build_cost': 1000,
                    'tech_start': ['test_tech'],
                    'items_needed': {'material': 2},
                    'services_needed': ['workshop'],
                    'items_build': {'test_item': 1}
                }
            }
        }
        
        self.manufacture_system = TManufacture(self.manufacturing_data)
        self.base_id = "test_base"
        self.manufacture_system.set_base_workshop_capacity(self.base_id, 10)

    def test_load_manufacturing_data(self):
        """Test loading manufacturing data."""
        self.assertIn('test_item', self.manufacture_system.entries)
        entry = self.manufacture_system.get_entry('test_item')
        self.assertEqual(entry.name, 'Test Item')
        self.assertEqual(entry.build_time, 5)
        self.assertEqual(entry.build_cost, 1000)

    def test_workshop_capacity_management(self):
        """Test workshop capacity management."""
        manager = self.manufacture_system.manufacturing_manager
        
        # Test initial capacity
        self.assertEqual(manager.get_base_workshop_capacity(self.base_id), 10)
        self.assertEqual(manager.get_used_workshop_capacity(self.base_id), 0)
        self.assertEqual(manager.get_available_workshop_capacity(self.base_id), 10)

    def test_project_requirements_validation(self):
        """Test project requirements validation."""
        entry = self.manufacture_system.get_entry('test_item')
        
        # Test with missing requirements
        can_start, issues = self.manufacture_system.validate_project_requirements(
            entry, self.base_id, 1, [], [], {}, 0
        )
        self.assertFalse(can_start)
        self.assertTrue(any('test_tech' in issue for issue in issues))
        self.assertTrue(any('workshop' in issue for issue in issues))
        self.assertTrue(any('material' in issue for issue in issues))
        self.assertTrue(any('funds' in issue for issue in issues))
        
        # Test with all requirements met
        can_start, issues = self.manufacture_system.validate_project_requirements(
            entry, self.base_id, 1, 
            ['test_tech'], ['workshop'], {'material': 5}, 2000
        )
        self.assertTrue(can_start)
        self.assertEqual(len(issues), 0)

    def test_start_manufacturing_project(self):
        """Test starting a manufacturing project."""
        success, result = self.manufacture_system.start_manufacturing_project(
            'test_item', self.base_id, 2,
            ['test_tech'], ['workshop'], {'material': 5}, 2000, 3
        )
        
        self.assertTrue(success)
        self.assertIsInstance(result, ManufacturingProject)
        self.assertEqual(result.quantity, 2)
        self.assertEqual(result.total_time, 10)  # 5 * 2
        self.assertEqual(result.workshop_capacity, 3)

    def test_daily_progress(self):
        """Test daily manufacturing progress."""
        # Start a project
        success, project = self.manufacture_system.start_manufacturing_project(
            'test_item', self.base_id, 2,
            ['test_tech'], ['workshop'], {'material': 5}, 2000, 5
        )
        self.assertTrue(success)
        
        # Process daily progress
        completed_items = self.manufacture_system.process_daily_manufacturing()
        
        # After 1 day with 5 capacity, should complete 1 item (5 man-days)
        self.assertIn(self.base_id, completed_items)
        completion = completed_items[self.base_id][0]
        self.assertEqual(completion['items_completed'], 1)
        self.assertEqual(completion['entry_id'], 'test_item')
        
        # Project should not be complete yet
        self.assertFalse(completion['project_completed'])
        self.assertEqual(project.items_completed, 1)

    def test_project_completion(self):
        """Test project completion."""
        # Start a small project that will complete quickly
        success, project = self.manufacture_system.start_manufacturing_project(
            'test_item', self.base_id, 1,
            ['test_tech'], ['workshop'], {'material': 5}, 2000, 10
        )
        self.assertTrue(success)
        
        # Process daily progress - should complete immediately
        completed_items = self.manufacture_system.process_daily_manufacturing()
        
        completion = completed_items[self.base_id][0]
        self.assertEqual(completion['items_completed'], 1)
        self.assertTrue(completion['project_completed'])
        self.assertTrue(project.is_completed())

    def test_multiple_projects(self):
        """Test managing multiple projects."""
        # Start two projects
        success1, project1 = self.manufacture_system.start_manufacturing_project(
            'test_item', self.base_id, 1,
            ['test_tech'], ['workshop'], {'material': 10}, 5000, 3
        )
        
        success2, project2 = self.manufacture_system.start_manufacturing_project(
            'test_item', self.base_id, 1,
            ['test_tech'], ['workshop'], {'material': 10}, 5000, 4
        )
        
        self.assertTrue(success1)
        self.assertTrue(success2)
        
        # Check capacity usage
        manager = self.manufacture_system.manufacturing_manager
        self.assertEqual(manager.get_used_workshop_capacity(self.base_id), 7)
        self.assertEqual(manager.get_available_workshop_capacity(self.base_id), 3)

    def test_insufficient_capacity(self):
        """Test handling of insufficient workshop capacity."""
        # Try to start a project that exceeds capacity
        success, result = self.manufacture_system.start_manufacturing_project(
            'test_item', self.base_id, 1,
            ['test_tech'], ['workshop'], {'material': 5}, 2000, 15  # More than available
        )
        
        self.assertFalse(success)
        self.assertIn('workshop capacity', result)

    def test_project_pause_resume(self):
        """Test pausing and resuming projects."""
        success, project = self.manufacture_system.start_manufacturing_project(
            'test_item', self.base_id, 1,
            ['test_tech'], ['workshop'], {'material': 5}, 2000, 3
        )
        self.assertTrue(success)
        
        # Pause project
        self.manufacture_system.pause_project(project.project_id)
        self.assertEqual(project.status, 'paused')
        
        # Resume project        self.manufacture_system.resume_project(project.project_id)
        self.assertEqual(project.status, 'active')

    def test_project_cancellation(self):
        """Test cancelling projects."""
        success, project = self.manufacture_system.start_manufacturing_project(
            'test_item', self.base_id, 1,
            ['test_tech'], ['workshop'], {'material': 5}, 2000, 3
        )
        self.assertTrue(success)
        
        # Cancel project
        self.manufacture_system.cancel_project(project.project_id)
        self.assertEqual(project.status, 'cancelled')

    def test_comprehensive_manufacturing_example(self):
        """Test comprehensive manufacturing example similar to the example_manufacturing.py."""
        # Set up more realistic manufacturing data
        manufacturing_data = {
            'manufacturing': {
                'pistol': {
                    'name': 'Combat Pistol',
                    'category': 'weapons',
                    'build_time': 5,  # 5 man-days per pistol
                    'build_cost': 1000,  # $1000 per pistol
                    'tech_start': ['basic_weapons'],
                    'items_needed': {'metal': 2, 'electronics': 1},  # per pistol
                    'services_needed': ['workshop'],
                    'items_build': {'pistol': 1}
                },
                'rifle': {
                    'name': 'Assault Rifle',
                    'category': 'weapons',
                    'build_time': 12,  # 12 man-days per rifle
                    'build_cost': 2500,
                    'tech_start': ['advanced_weapons'],
                    'items_needed': {'metal': 5, 'electronics': 2, 'polymer': 1},
                    'services_needed': ['workshop', 'precision_tools'],
                    'items_build': {'rifle': 1}
                },
                'medkit': {
                    'name': 'Medical Kit',
                    'category': 'supplies',
                    'build_time': 2,  # 2 man-days per medkit
                    'build_cost': 500,
                    'tech_start': ['basic_medicine'],
                    'items_needed': {'chemicals': 3, 'textiles': 1},
                    'services_needed': ['medical_lab'],
                    'items_build': {'medkit': 1}
                }
            }
        }
        
        # Initialize manufacturing system with comprehensive data
        comprehensive_system = TManufacture(manufacturing_data)
        base_id = "comprehensive_base"
        comprehensive_system.set_base_workshop_capacity(base_id, 10)  # 10 man-days per day
        
        # Example: Player wants to build items
        available_tech = ['basic_weapons', 'basic_medicine']
        available_services = ['workshop', 'medical_lab']
        available_items = {'metal': 20, 'electronics': 10, 'chemicals': 15, 'textiles': 10, 'polymer': 5}
        available_money = 50000
        
        # Test getting available projects
        available_projects = comprehensive_system.get_available_projects(
            available_tech, available_services, available_items
        )
        
        # Should have pistol and medkit available (not rifle due to missing advanced_weapons tech)
        available_project_ids = [p.pid for p in available_projects]
        self.assertIn('pistol', available_project_ids)
        self.assertIn('medkit', available_project_ids)
        self.assertNotIn('rifle', available_project_ids)  # Missing advanced_weapons tech
        
        # Start manufacturing 3 pistols
        success1, project1 = comprehensive_system.start_manufacturing_project(
            'pistol', base_id, 3, 
            available_tech, available_services, available_items, available_money,
            workshop_capacity=2  # Allocate 2 man-days per day to this project
        )
        
        self.assertTrue(success1)
        self.assertEqual(project1.quantity, 3)
        self.assertEqual(project1.total_time, 15)  # 5 * 3
        self.assertEqual(project1.workshop_capacity, 2)
        
        # Start manufacturing 5 medkits
        success2, project2 = comprehensive_system.start_manufacturing_project(
            'medkit', base_id, 5,
            available_tech, available_services, available_items, available_money,
            workshop_capacity=3
        )
        
        self.assertTrue(success2)
        self.assertEqual(project2.quantity, 5)
        self.assertEqual(project2.total_time, 10)  # 2 * 5
        self.assertEqual(project2.workshop_capacity, 3)
        
        # Check manufacturing status
        status = comprehensive_system.get_manufacturing_status(base_id)
        self.assertEqual(status['total_capacity'], 10)
        self.assertEqual(status['used_capacity'], 5)  # 2 + 3
        self.assertEqual(status['available_capacity'], 5)  # 10 - 5
        self.assertEqual(status['active_projects'], 2)
        
        # Test daily progress simulation
        daily_results = []
        for day in range(1, 8):  # Simulate 7 days
            completed_items = comprehensive_system.process_daily_manufacturing()
            daily_results.append((day, completed_items))
            
            # Verify progress tracking
            if completed_items and base_id in completed_items:
                for completion in completed_items[base_id]:
                    self.assertIn('items_completed', completion)
                    self.assertIn('entry_id', completion)
                    self.assertIn('project_completed', completion)
        
        # After 5 days, medkits should be complete (10 man-days / 3 per day = 3.33 days)
        # After 8 days, pistols should be complete (15 man-days / 2 per day = 7.5 days)
        
        # Check that both projects eventually complete
        final_status = comprehensive_system.get_manufacturing_status(base_id)
        completed_projects = [p for p in final_status['projects'] if p.is_completed()]
        
        # At least one project should be completed by day 7
        self.assertGreater(len(completed_projects), 0)
        
        # Verify total items produced
        total_pistols = sum(p.items_completed for p in final_status['projects'] if p.entry_id == 'pistol')
        total_medkits = sum(p.items_completed for p in final_status['projects'] if p.entry_id == 'medkit')
        
        # Should have made progress on both
        self.assertGreater(total_pistols, 0)
        self.assertGreater(total_medkits, 0)

    def test_resource_consumption_validation(self):
        """Test that the system properly validates resource consumption."""
        # Test with insufficient materials
        entry = self.manufacture_system.get_entry('test_item')
        
        # Try to build more items than materials allow
        insufficient_items = {'material': 1}  # Need 2 per item, trying to build 1
        can_start, issues = self.manufacture_system.validate_project_requirements(
            entry, self.base_id, 1, 
            ['test_tech'], ['workshop'], insufficient_items, 2000
        )
        
        self.assertFalse(can_start)
        self.assertTrue(any('material' in issue for issue in issues))

    def test_cost_calculation(self):
        """Test manufacturing cost calculations."""
        entry = self.manufacture_system.get_entry('test_item')
        
        # Test cost calculation for different quantities
        can_afford_1, cost_1 = self.manufacture_system.can_afford_project(entry, 1, 1000)
        self.assertTrue(can_afford_1)
        self.assertEqual(cost_1, 1000)
        
        can_afford_3, cost_3 = self.manufacture_system.can_afford_project(entry, 3, 2000)
        self.assertFalse(can_afford_3)  # Need 3000, have 2000
        self.assertEqual(cost_3, 3000)
          can_afford_3_rich, cost_3_rich = self.manufacture_system.can_afford_project(entry, 3, 5000)
        self.assertTrue(can_afford_3_rich)
        self.assertEqual(cost_3_rich, 3000)

    def run_example_demonstration(self):
        """
        Run a demonstration similar to example_manufacturing.py.
        This method can be called to show the system in action.
        """
        print("\n=== Manufacturing System Demonstration ===")
        
        # Set up comprehensive manufacturing data
        manufacturing_data = {
            'manufacturing': {
                'pistol': {
                    'name': 'Combat Pistol',
                    'category': 'weapons',
                    'build_time': 5,
                    'build_cost': 1000,
                    'tech_start': ['basic_weapons'],
                    'items_needed': {'metal': 2, 'electronics': 1},
                    'services_needed': ['workshop'],
                    'items_build': {'pistol': 1}
                },
                'medkit': {
                    'name': 'Medical Kit',
                    'category': 'supplies',
                    'build_time': 2,
                    'build_cost': 500,
                    'tech_start': ['basic_medicine'],
                    'items_needed': {'chemicals': 3, 'textiles': 1},
                    'services_needed': ['medical_lab'],
                    'items_build': {'medkit': 1}
                }
            }
        }
        
        demo_system = TManufacture(manufacturing_data)
        base_id = "demo_base"
        demo_system.set_base_workshop_capacity(base_id, 10)
        
        # Resources
        available_tech = ['basic_weapons', 'basic_medicine']
        available_services = ['workshop', 'medical_lab']
        available_items = {'metal': 10, 'electronics': 5, 'chemicals': 15, 'textiles': 10}
        available_money = 10000
        
        print(f"Base capacity: {demo_system.manufacturing_manager.get_base_workshop_capacity(base_id)} man-days/day")
        print(f"Available resources: ${available_money}, {available_items}")
        
        # Start projects
        success1, project1 = demo_system.start_manufacturing_project(
            'pistol', base_id, 2, available_tech, available_services, 
            available_items, available_money, 3
        )
        
        success2, project2 = demo_system.start_manufacturing_project(
            'medkit', base_id, 3, available_tech, available_services,
            available_items, available_money, 2
        )
        
        if success1:
            print(f"Started pistol project: {project1.quantity} items, {project1.total_time} man-days")
        if success2:
            print(f"Started medkit project: {project2.quantity} items, {project2.total_time} man-days")
        
        # Simulate progress
        print("\nDaily progress:")
        for day in range(1, 6):
            completed = demo_system.process_daily_manufacturing()
            print(f"Day {day}: {len(completed.get(base_id, []))} completions")
            
            if completed and base_id in completed:
                for completion in completed[base_id]:
                    print(f"  Completed {completion['items_completed']} {completion['entry_id']}")
        
        print("=== Demonstration Complete ===\n")


if __name__ == '__main__':
    unittest.main()
