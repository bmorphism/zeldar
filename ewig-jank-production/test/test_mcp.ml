open Mcp

let test_message_creation () =
  let msg = create_message ~id:"test-1" ~method_:"initialize" () in
  assert (msg.jsonrpc = "2.0");
  assert (msg.id = Some "test-1");
  assert (msg.method_ = "initialize");
  print_endline "✓ Message creation test passed"

let test_json_conversion () =
  let msg = create_message ~id:"test-2" ~method_:"resources/list" () in
  let json = message_to_json msg in
  let parsed_msg = message_of_json json in
  assert (parsed_msg.jsonrpc = msg.jsonrpc);
  assert (parsed_msg.id = msg.id);
  assert (parsed_msg.method_ = msg.method_);
  print_endline "✓ JSON conversion test passed"

let test_server () =
  let server = Server.create () in
  assert (not (Server.is_initialized server));
  
  let resource = {
    uri = "test://resource";
    name = "Test Resource";
    description = None;
    mime_type = Some "text/plain";
  } in
  
  let tool = {
    name = "test_tool";
    description = "A test tool";
    input_schema = `Assoc [("type", `String "object")];
  } in
  
  Server.add_resource server resource;
  Server.add_tool server tool;
  Server.set_initialized server;
  
  assert (Server.is_initialized server);
  print_endline "✓ Server test passed"

let () =
  print_endline "Running MCP tests...";
  test_message_creation ();
  test_json_conversion ();
  test_server ();
  print_endline "All tests passed! 🎉"

