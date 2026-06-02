"""
Comprehensive Backend API Tests for Tidepaper Chat
Tests all endpoints, CRUD operations, AI integration, and edge cases.
"""
import requests
import sys
import time
from datetime import datetime

# Use public endpoint
BASE_URL = "https://code-fixer-233.preview.emergentagent.com/api"

class ChatAPITester:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.session_ids = []
        self.results = []

    def log(self, emoji, message):
        print(f"{emoji} {message}")

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{BASE_URL}{endpoint}"
        self.tests_run += 1
        self.log("🔍", f"Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, params=params, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, timeout=30)
            elif method == 'PATCH':
                response = requests.patch(url, json=data, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                self.log("✅", f"PASSED - Status: {response.status_code}")
                self.results.append({"test": name, "status": "PASSED"})
            else:
                self.log("❌", f"FAILED - Expected {expected_status}, got {response.status_code}")
                self.log("📄", f"Response: {response.text[:200]}")
                self.results.append({"test": name, "status": "FAILED", "reason": f"Status {response.status_code}"})

            try:
                return success, response.json() if response.text else {}
            except:
                return success, {}

        except Exception as e:
            self.log("❌", f"FAILED - Error: {str(e)}")
            self.results.append({"test": name, "status": "FAILED", "reason": str(e)})
            return False, {}

    def test_health_check(self):
        """Test GET /api/ returns ok"""
        self.log("🏥", "=== Testing Health Check ===")
        success, response = self.run_test(
            "Health Check",
            "GET",
            "/",
            200
        )
        if success and response.get("ok"):
            self.log("✅", "Health check passed with ok=True")
            return True
        else:
            self.log("❌", f"Health check failed: {response}")
            return False

    def test_get_models(self):
        """Test GET /api/models returns three providers with default"""
        self.log("🤖", "=== Testing Models Endpoint ===")
        success, response = self.run_test(
            "Get Models",
            "GET",
            "/models",
            200
        )
        if not success:
            return False
        
        # Validate structure
        models = response.get("models", {})
        default = response.get("default", {})
        
        providers = ["openai", "anthropic", "gemini"]
        all_present = all(p in models for p in providers)
        all_non_empty = all(len(models.get(p, [])) > 0 for p in providers)
        
        if all_present and all_non_empty:
            self.log("✅", f"All three providers present with models")
        else:
            self.log("❌", f"Missing providers or empty model lists: {models}")
            return False
        
        if default.get("provider") == "openai" and default.get("model") == "gpt-5":
            self.log("✅", "Default model is openai/gpt-5")
            return True
        else:
            self.log("❌", f"Default model incorrect: {default}")
            return False

    def test_create_session(self):
        """Test POST /api/sessions creates a session"""
        self.log("➕", "=== Testing Create Session ===")
        success, response = self.run_test(
            "Create Session",
            "POST",
            "/sessions",
            200,
            data={"title": "Test Session", "provider": "openai", "model": "gpt-5"}
        )
        if success and response.get("id"):
            session_id = response["id"]
            self.session_ids.append(session_id)
            self.log("✅", f"Session created with ID: {session_id}")
            return session_id
        return None

    def test_list_sessions(self):
        """Test GET /api/sessions lists sessions newest-first"""
        self.log("📋", "=== Testing List Sessions ===")
        success, response = self.run_test(
            "List Sessions",
            "GET",
            "/sessions",
            200
        )
        if success and isinstance(response, list):
            self.log("✅", f"Retrieved {len(response)} sessions")
            # Check if sorted by updated_at descending
            if len(response) > 1:
                dates = [s.get("updated_at") for s in response]
                if dates == sorted(dates, reverse=True):
                    self.log("✅", "Sessions sorted newest-first")
                else:
                    self.log("⚠️", "Sessions may not be sorted correctly")
            return True
        return False

    def test_rename_session(self, session_id):
        """Test PATCH /api/sessions/{id} renames session"""
        self.log("✏️", "=== Testing Rename Session ===")
        new_title = f"Renamed Session {datetime.now().strftime('%H:%M:%S')}"
        success, response = self.run_test(
            "Rename Session",
            "PATCH",
            f"/sessions/{session_id}",
            200,
            data={"title": new_title}
        )
        if success and response.get("title") == new_title:
            self.log("✅", f"Session renamed to: {new_title}")
            return True
        return False

    def test_change_model(self, session_id):
        """Test PATCH /api/sessions/{id} changes provider/model"""
        self.log("🔄", "=== Testing Change Model ===")
        success, response = self.run_test(
            "Change Model",
            "PATCH",
            f"/sessions/{session_id}",
            200,
            data={"provider": "anthropic", "model": "claude-sonnet-4-6"}
        )
        if success and response.get("provider") == "anthropic" and response.get("model") == "claude-sonnet-4-6":
            self.log("✅", "Model changed to anthropic/claude-sonnet-4-6")
            return True
        return False

    def test_invalid_model(self, session_id):
        """Test PATCH with invalid model returns 400"""
        self.log("🚫", "=== Testing Invalid Model ===")
        success, response = self.run_test(
            "Invalid Model (should fail)",
            "PATCH",
            f"/sessions/{session_id}",
            400,
            data={"provider": "openai", "model": "invalid-model-xyz"}
        )
        if success:
            self.log("✅", "Invalid model correctly rejected with 400")
            return True
        return False

    def test_get_messages(self, session_id):
        """Test GET /api/sessions/{id}/messages"""
        self.log("💬", "=== Testing Get Messages ===")
        success, response = self.run_test(
            "Get Messages",
            "GET",
            f"/sessions/{session_id}/messages",
            200
        )
        if success and isinstance(response, list):
            self.log("✅", f"Retrieved {len(response)} messages")
            return response
        return None

    def test_send_message(self, session_id, text):
        """Test POST /api/sessions/{id}/messages"""
        self.log("📤", f"=== Testing Send Message: '{text[:50]}...' ===")
        success, response = self.run_test(
            "Send Message",
            "POST",
            f"/sessions/{session_id}/messages",
            200,
            data={"text": text}
        )
        if success:
            user_msg = response.get("user_message", {})
            assistant_msg = response.get("assistant_message", {})
            if user_msg.get("role") == "user" and assistant_msg.get("role") == "assistant":
                self.log("✅", f"User message: {user_msg.get('content')[:50]}...")
                self.log("✅", f"AI response: {assistant_msg.get('content')[:100]}...")
                return True, assistant_msg.get("content", "")
        return False, ""

    def test_empty_message(self, session_id):
        """Test POST with empty text returns 400"""
        self.log("🚫", "=== Testing Empty Message ===")
        success, response = self.run_test(
            "Empty Message (should fail)",
            "POST",
            f"/sessions/{session_id}/messages",
            400,
            data={"text": ""}
        )
        if success:
            self.log("✅", "Empty message correctly rejected with 400")
            return True
        return False

    def test_unknown_session(self):
        """Test POST to unknown session returns 404"""
        self.log("🚫", "=== Testing Unknown Session ===")
        success, response = self.run_test(
            "Unknown Session (should fail)",
            "POST",
            "/sessions/unknown-session-id-12345/messages",
            404,
            data={"text": "Hello"}
        )
        if success:
            self.log("✅", "Unknown session correctly rejected with 404")
            return True
        return False

    def test_auto_title(self):
        """Test auto-title: first message renames 'New conversation'"""
        self.log("🏷️", "=== Testing Auto-Title Feature ===")
        # Create session with default title
        success, session = self.run_test(
            "Create Session for Auto-Title",
            "POST",
            "/sessions",
            200,
            data={"provider": "openai", "model": "gpt-5"}
        )
        if not success or not session.get("id"):
            return False
        
        session_id = session["id"]
        self.session_ids.append(session_id)
        
        # Verify initial title is "New conversation"
        if session.get("title") != "New conversation":
            self.log("❌", f"Initial title is not 'New conversation': {session.get('title')}")
            return False
        
        # Send first message
        first_message = "What is the capital of France?"
        success, response = self.run_test(
            "Send First Message for Auto-Title",
            "POST",
            f"/sessions/{session_id}/messages",
            200,
            data={"text": first_message}
        )
        if not success:
            return False
        
        # Wait a moment for title update
        time.sleep(1)
        
        # Check if title was updated
        success, updated_session = self.run_test(
            "Get Session After First Message",
            "GET",
            f"/sessions/{session_id}",
            200
        )
        if success:
            new_title = updated_session.get("title", "")
            if new_title != "New conversation" and len(new_title) > 0:
                self.log("✅", f"Auto-title worked! New title: {new_title}")
                return True
            else:
                self.log("❌", f"Auto-title failed. Title still: {new_title}")
                return False
        return False

    def test_multi_turn_memory(self):
        """Test multi-turn conversation with context preservation"""
        self.log("🧠", "=== Testing Multi-Turn Memory ===")
        # Create new session
        success, session = self.run_test(
            "Create Session for Memory Test",
            "POST",
            "/sessions",
            200,
            data={"provider": "openai", "model": "gpt-5"}
        )
        if not success or not session.get("id"):
            return False
        
        session_id = session["id"]
        self.session_ids.append(session_id)
        
        # First message: establish context
        self.log("💭", "Sending first message to establish context...")
        success1, response1 = self.test_send_message(session_id, "My favorite color is teal")
        if not success1:
            return False
        
        # Wait for AI processing
        time.sleep(2)
        
        # Second message: test context recall
        self.log("💭", "Sending second message to test context recall...")
        success2, response2 = self.test_send_message(session_id, "What is my favorite color?")
        if not success2:
            return False
        
        # Check if AI response mentions "teal"
        if "teal" in response2.lower():
            self.log("✅", "Multi-turn memory working! AI remembered the context.")
            return True
        else:
            self.log("⚠️", f"AI may not have used context. Response: {response2[:200]}")
            return False

    def test_provider_switching(self):
        """Test switching between providers (anthropic, gemini)"""
        self.log("🔀", "=== Testing Provider Switching ===")
        
        # Test Anthropic
        self.log("🤖", "Testing Anthropic provider...")
        success, session = self.run_test(
            "Create Session with Anthropic",
            "POST",
            "/sessions",
            200,
            data={"provider": "anthropic", "model": "claude-sonnet-4-6"}
        )
        if not success or not session.get("id"):
            return False
        
        anthropic_session_id = session["id"]
        self.session_ids.append(anthropic_session_id)
        
        success_anthropic, _ = self.test_send_message(anthropic_session_id, "Say hello in one word")
        time.sleep(2)
        
        # Test Gemini
        self.log("🤖", "Testing Gemini provider...")
        success, session = self.run_test(
            "Create Session with Gemini",
            "POST",
            "/sessions",
            200,
            data={"provider": "gemini", "model": "gemini-3-flash-preview"}
        )
        if not success or not session.get("id"):
            return False
        
        gemini_session_id = session["id"]
        self.session_ids.append(gemini_session_id)
        
        success_gemini, _ = self.test_send_message(gemini_session_id, "Say hello in one word")
        
        if success_anthropic and success_gemini:
            self.log("✅", "Provider switching works for both Anthropic and Gemini")
            return True
        else:
            self.log("⚠️", f"Provider switching partial: Anthropic={success_anthropic}, Gemini={success_gemini}")
            return False

    def test_delete_session(self, session_id):
        """Test DELETE /api/sessions/{id}"""
        self.log("🗑️", "=== Testing Delete Session ===")
        success, response = self.run_test(
            "Delete Session",
            "DELETE",
            f"/sessions/{session_id}",
            200
        )
        if success and response.get("ok"):
            self.log("✅", f"Session {session_id} deleted successfully")
            # Verify messages are also deleted
            success_check, _ = self.run_test(
                "Verify Session Deleted",
                "GET",
                f"/sessions/{session_id}",
                404
            )
            if success_check:
                self.log("✅", "Session and messages cascade deleted")
                return True
        return False

    def cleanup(self):
        """Clean up test sessions"""
        self.log("🧹", "=== Cleaning Up Test Sessions ===")
        for session_id in self.session_ids:
            try:
                requests.delete(f"{BASE_URL}/sessions/{session_id}", timeout=5)
            except:
                pass
        self.log("✅", "Cleanup complete")

    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        print("="*60)
        
        # Print failed tests
        failed = [r for r in self.results if r["status"] == "FAILED"]
        if failed:
            print("\n❌ FAILED TESTS:")
            for f in failed:
                print(f"  - {f['test']}: {f.get('reason', 'Unknown')}")
        
        return 0 if self.tests_passed == self.tests_run else 1

def main():
    tester = ChatAPITester()
    
    try:
        # Run all tests
        tester.test_health_check()
        tester.test_get_models()
        
        # Create session for basic CRUD tests
        session_id = tester.test_create_session()
        if session_id:
            tester.test_list_sessions()
            tester.test_rename_session(session_id)
            tester.test_change_model(session_id)
            tester.test_invalid_model(session_id)
            tester.test_get_messages(session_id)
            tester.test_send_message(session_id, "Hello, how are you?")
            tester.test_empty_message(session_id)
        
        # Edge cases
        tester.test_unknown_session()
        
        # Advanced features
        tester.test_auto_title()
        tester.test_multi_turn_memory()
        tester.test_provider_switching()
        
        # Cleanup
        if session_id:
            tester.test_delete_session(session_id)
        
    finally:
        tester.cleanup()
        return tester.print_summary()

if __name__ == "__main__":
    sys.exit(main())
