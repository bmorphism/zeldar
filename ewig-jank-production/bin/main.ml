open Lwt.Syntax
open Mcp

let example_resource = {
  uri = "example://resource/1";
  name = "Example Resource";
  description = Some "An example resource for demonstration";
  mime_type = Some "text/plain";
}

let example_tool = {
  name = "echo";
  description = "Echoes back the input";
  input_schema = `Assoc [
    ("type", `String "object");
    ("properties", `Assoc [
      ("message", `Assoc [
        ("type", `String "string");
        ("description", `String "Message to echo back")
      ])
    ]);
    ("required", `List [`String "message"])
  ];
}

let run_server () =
  let* () = Lwt_io.printl "Starting MCP server example..." in
  let server = Server.create () in
  
  (* Add example resources and tools *)
  Server.add_resource server example_resource;
  Server.add_tool server example_tool;
  Server.set_initialized server;
  
  let* () = Lwt_io.printf "Server initialized: %b\n" (Server.is_initialized server) in
  let* () = Lwt_io.printl "Protocol version: " in
  let* () = Lwt_io.printl protocol_version in
  
  (* Create an example message *)
  let msg = create_message ~id:"1" ~method_:"resources/list" () in
  let json = message_to_json msg in
  let* () = Lwt_io.printl "Example message:" in
  let* () = Lwt_io.printl (Yojson.Safe.pretty_to_string json) in
  
  Lwt.return ()

let () =
  Lwt_main.run (run_server ())

