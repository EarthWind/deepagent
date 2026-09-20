# Octop 源码索引

调研日期：2026-09-20。Octop 固定提交：`757fd12e5dcae7f9303dbfbbf6321a6986694a8b`。

Octop 链接固定到提交；依赖按 `uv.lock` 的发行源码包和 SHA-256 固定。依赖条目的行号指解压后的原文件，不把 GitHub main 当成锁定版本。

<a id="project"></a>
## project

[pyproject.toml](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/pyproject.toml) · 217 行

<a id="lock"></a>
## lock

[uv.lock](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/uv.lock) · 5342 行

<a id="readme"></a>
## readme

[README.md](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/README.md) · 548 行

<a id="architecture"></a>
## architecture

[docs/architecture.md](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/docs/architecture.md) · 168 行

<a id="adr"></a>
## adr

[docs/adr/001-single-process-model.md](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/docs/adr/001-single-process-model.md) · 35 行

<a id="server"></a>
## server

[src/octop/infra/server.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/server.py) · 585 行

`SizeTimedRotatingFileHandler` L46–86；`gzip_rotated_log` L89–103；`_parse_log_compress` L106–108；`delaycompress_rotated_logs` L111–137；`_parse_log_retention_days` L140–147；`_parse_log_max_bytes` L150–157；`_build_log_handler` L160–180；`_purge_stale_logs` L183–196；`_attach_log_handler` L199–205；`AppRuntime` L209–239；`OctopServer` L242–585；`__init__` L49–59；`shouldRollover` L61–69；`rotate` L71–75；`rotation_filename` L77–86；`replace_services` L220–239；`__init__` L243–255；`user_manager` L259–260；`sso_service` L263–275；`database_bound` L278–279；`start` L281–332；`bind_control_plane` L334–360；`_boot_runtime` L362–490；`_emit_wizard_password` L492–520；`stop` L522–541；`_setup_logging` L545–581；`_ensure_jwt_secret` L583–585

<a id="launch"></a>
## launch

[src/octop/launch.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/launch.py) · 156 行

`_ensure_linux_bubblewrap` L16–30；`_schedule_linux_bubblewrap_ensure` L33–40；`_cancel_background_task` L43–49；`_serve` L52–53；`run_foreground` L56–151；`run_foreground_blocking` L154–156

<a id="manager"></a>
## manager

[src/octop/infra/agents/manager.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/agents/manager.py) · 2962 行

`_memory_namespace` L100–101；`skills_disabled_set` L104–109；`tools_disabled_set` L112–116；`skill_package_ids_list` L119–124；`_memory_aux_model_settings` L127–154；`_memory_extract_settings` L157–211；`_resolve_memory_backend_kwargs` L214–220；`_fill_missing_subagent_colors` L223–245；`validate_custom_agent_id` L258–269；`AgentCreateSpec` L278–300；`AgentManager` L308–2962；`__init__` L331–388；`replace_persistence` L390–413；`set_cron_manager` L415–417；`set_proactive_scheduler` L419–421；`set_team_processor` L423–425；`boot` L427–450；`shutdown` L452–459；`providers` L466–467；`security` L470–471；`acp_settings` L474–475；`tool_guard_rules` L478–479；`langfuse` L482–483；`media_generation` L486–487；`paths` L490–491；`harness_manager` L494–495；`octop_config` L498–499；`create` L505–631；`_preserve_system_files_path` L633–646；`update` L648–703；`set_shared` L705–711；`set_icon_url` L713–722；`delete` L724–742；`start` L744–750；`stop` L752–760；`_quiesce_harness_memory` L762–785；`_wait_memory_maintenance_idle` L788–803；`get_row` L809–811；`workspace_for_agent` L813–828；`list_agents` L830–831；`list_rows` L833–835；`resolve_user_agent` L837–851；`get_config` L853–858；`persist_harness_config` L860–877；`resolve_workspace_dir` L879–901；`is_bootstrapped` L903–915；`find_agents_using_provider` L917–923；`find_agents_using_storage_backend` L925–933；`get_agent` L939–952；`_unavailable_error` L954–962；`delete_thread_checkpoint` L964–993；`is_agent_active` L999–1001；`try_begin_history_backfill` L1003–1012；`end_history_backfill` L1014–1018；`_begin_invocation` L1020–1031；`_end_invocation` L1033–1038；`_track_invocation` L1041–1046；`stream` L1048–1058；`call` L1060–1071；`resume_hitl` L1073–1086；`cancel_stream` L1088–1091；`get_thread_model` L1093–1096；`set_thread_model` L1098–1100；`clear_thread_model` L1102–1104；`resolve_fallback_model_ref` L1106–1113；`reload` L1119–1121；`reload_all` L1123–1128；`reload_harness_agents` L1130–1136；`_agent_uses_auto_default` L1138–1140；`_provider_reload_impact_ids` L1142–1172；`_reload_agents` L1174–1187；`on_provider_changed` L1189–1216；`reload_connectors` L1222–1248；`reload_connectors_for_user` L1250–1260；`invalidate_mcp_tool_cache` L1262–1271；`mcp_server_labels_for_user` L1273–1279；`resolve_tool_display_name_for_chat` L1281–1301；`_server_lock` L1303–1310；`_get_or_load_mcp_tools` L1312–1371；`merge_turn_mcp_servers` L1373–1387；`default_mcp_servers` L1389–1394；`default_knowledge_base_ids` L1396–1401；`prepare_chat_mcp` L1403–1574；`_attach_gateway_tools` L1576–1611；`save_langfuse` L1617–1634；`save_media_generation` L1636–1656；`save_security` L1658–1666；`apply_persona_mbti` L1672–1701；`update_config_json` L1703–1716；`persist_skills_disabled` L1718–1727；`persist_tools_disabled` L1729–1737；`persist_plugin_tools_config` L1739–1748；`_resolve_skill_package_dirs` L1750–1761；`_normalize_skills_dir_config` L1764–1775；`_backend_supports_host_skill_packages` L1778–1804；`persist_skill_package_ids` L1806–1832；`sync_skill_package_dirs` L1834–1864；`validate_skill_package_ids` L1866–1875；`persist_knowledge_base_ids` L1877–1890；`persist_mcp_servers` L1892–1905；`validate_knowledge_base_ids` L1907–1919；`validate_mcp_servers` L1921–1929；`assert_backend_supports_skill_packages` L1931–1955；`refresh_agents_for_package` L1957–1962；`strip_skill_package_id` L1964–1977；`resolve_context_max_tokens` L1979–1981；`list_skill_summaries` L1983–2136；`list_subagent_summaries` L2138–2143；`sync_skills_disabled` L2145–2147；`sync_tools_disabled` L2149–2161；`sync_effective_tools_disabled` L2163–2181；`_assert_agent_name_available` L2187–2201；`_complete_create_bootstrap` L2207–2219；`_start_agent` L2221–2248；`_post_start_agent` L2250–2310；`_mark_bootstrap_graph_refresh_pending` L2312–2324；`_apply_pending_bootstrap_graph_refresh` L2326–2342；`_agent_config_dict` L2344–2346；`_backend_spec_for_row` L2348–2368；`resolved_backend_spec` L2370–2375；`_owner_username` L2377–2383；`_spec_is_opensandbox` L2386–2387；`_prepare_docker_backend` L2389–2400；`_backend_workspace_for_row` L2402–2438；`_seed_expert_template` L2440–2504；`_reload_agent` L2510–2536；`_schedule_reload` L2538–2544；`_reload_worker` L2546–2559；`_agent_runtime_bundle` L2565–2596；`_refresh_peer_entry` L2598–2602；`_apply_peer_profile_metadata` L2604–2621；`_peer_manifest_metadata` L2623–2651；`_connector_uid_for` L2653–2664；`_prepare_stream_request` L2666–2681；`_build_harness_config` L2683–2962；`_one` L1180–1185；`_on_bootstrap_complete` L2307–2308

<a id="processor"></a>
## processor

[src/octop/infra/gateway/process/processor.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/gateway/process/processor.py) · 1537 行

`_stream_error` L84–87；`_MessageEventSink` L90–100；`GlobalProcessor` L103–1494；`_octop_user_id` L1497–1503；`_peer_turn_messages` L1506–1527；`_mcp_server_names` L1530–1537；`__init__` L91–92；`text` L94–97；`complete` L99–100；`__init__` L106–147；`_begin_history` L149–193；`_finish_history` L195–201；`_complete_resumed_history` L203–210；`hitl_coordinator` L213–214；`replace_thread_message_repo` L216–218；`_agent_trajectory_enabled` L220–226；`_observe_trajectory` L228–250；`_finish_trajectory` L252–270；`_observe_turn_start_context` L272–337；`_trajectory_system_prompt` L339–355；`_trajectory_enabled_skill_names` L357–383；`_trajectory_workspace_files` L385–407；`prepare_peer_session` L411–434；`record_peer_turn` L436–464；`compose_followup` L466–481；`on_reply` L483–499；`_deliver_team_text` L501–511；`_peer_display_name` L513–515；`_slash_ctx` L517–541；`_model_ref_from_meta` L544–556；`_resolve_harness_model` L558–607；`_resolve_reasoning_overrides` L609–648；`__call__` L652–918；`iter_turn_chunks` L923–1125；`iter_hitl_resume_chunks` L1127–1188；`_build_dashboard_request` L1190–1303；`_attach_turn_knowledge_config` L1305–1332；`_resolve_turn_mcp_servers` L1334–1375；`_record_stream_error` L1377–1389；`_touch_thread_after_turn` L1391–1394；`_record_turn_usage` L1396–1412；`_persist_incomplete_turn` L1414–1423；`_record_turn_history` L1425–1454；`_append_slash_checkpoint` L1456–1494

<a id="request"></a>
## request

[src/octop/infra/gateway/process/harness_request.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/gateway/process/harness_request.py) · 332 行

`_workspace_from_media_backend` L23–26；`_group_turn_text` L29–93；`build_content_from_message` L96–164；`content_from_parts` L167–194；`build_content` L197–210；`_build_content_sync` L213–252；`build_harness_request` L255–322；`sender_label` L44–54

<a id="gateway"></a>
## gateway

[src/octop/infra/gateway/gateway.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/gateway/gateway.py) · 680 行

`SlashRuntimeMeta` L57–59；`ChannelRuntimeStatus` L63–74；`ChannelCreateSpec` L78–84；`_probe_processor` L87–90；`Gateway` L93–680；`__init__` L100–125；`replace_repos` L127–135；`ws_hub` L138–139；`cli_hub` L142–143；`cli_channel_id` L146–147；`channel_manager` L150–151；`dashboard_channel_id` L154–155；`slash_dispatcher` L158–159；`processor` L162–165；`history_backfill` L168–169；`slash_meta` L172–173；`set_slash_meta` L175–176；`thread_registry` L179–180；`get_runtime_status` L182–183；`runtime_status_to_dict` L185–200；`boot` L202–243；`refresh_media_backends` L245–260；`reload_channels_from_db` L262–286；`shutdown` L288–296；`list_channels` L298–299；`get_channel` L301–302；`create_channel` L304–337；`update_channel` L339–361；`delete_channel` L363–366；`require_session` L368–375；`_bump_virtual_session` L377–381；`run_in_session` L383–393；`push_text_from_session` L395–409；`push_session_text` L411–430；`_channel_id_for_session` L433–442；`_resolve_push_subject` L444–461；`notify_dashboard_push` L463–484；`_require_channel_manager` L486–489；`_preempt_cancel_on_stop` L491–520；`push_text` L522–530；`probe_channel` L532–539；`probe_config` L541–563；`_probe_row` L565–594；`_format_probe_error` L597–606；`_set_runtime_status` L608–621；`_safe_register_channel` L623–630；`_register_channel` L632–655；`_config_from_row` L657–671；`_unregister` L673–680；`_locked` L403–407

<a id="threads"></a>
## threads

[src/octop/infra/gateway/threads.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/gateway/threads.py) · 438 行

`ThreadRegistry` L13–423；`_new_thread_id` L426–427；`thread_row_has_messages` L430–438；`make_key` L22–30；`peer_session_key` L33–46；`dashboard_key` L49–55；`cli_key` L58–64；`__init__` L66–69；`replace_repos` L71–74；`_refresh_session_if_needed` L76–105；`get_or_create` L107–163；`get_or_create_by_key` L165–195；`get_bound_thread_id` L197–199；`get_session` L201–202；`rebind` L204–245；`reset` L247–291；`reset_by_session_key` L293–320；`set_title_if_null` L322–323；`update_title` L325–326；`set_pinned` L328–329；`update_composer` L331–344；`touch_last_active` L346–347；`append_artifacts` L349–350；`get_thread` L352–353；`list_threads` L355–356；`list_threads_for_session` L358–359；`create_thread` L361–383；`ensure_thread` L385–405；`delete_thread` L407–408；`increment_unread` L410–411；`mark_thread_read` L413–414；`mark_agent_read` L416–417；`unread_totals_by_agent` L419–420；`unread_counts_for_threads` L422–423

<a id="chat-ws"></a>
## chat-ws

[src/octop/api/routers/chat/ws.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/api/routers/chat/ws.py) · 183 行

`dashboard_chat_ws` L33–183；`send_frame` L70–75

<a id="chat-turn"></a>
## chat-turn

[src/octop/api/routers/chat/turn.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/api/routers/chat/turn.py) · 354 行

`PreparedDashboardTurn` L49–57；`resolve_thread_id` L60–86；`_turn_plain_text` L89–107；`_message_content_nonempty` L110–123；`turn_has_content` L126–134；`_mime_from_block` L137–144；`_workspace_path_from_block` L147–152；`content_parts_from_dashboard_turn` L155–223；`prepare_dashboard_turn` L226–303；`build_dashboard_inbound` L306–349；`merge_turn_target_agents` L352–354

<a id="chat-routes"></a>
## chat-routes

[src/octop/api/routers/chat/routes.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/api/routers/chat/routes.py) · 255 行

`get_chat_welcome` L55–90；`iter_dashboard_hitl_resume_sse` L93–147；`_dashboard_hitl_stream_context` L150–163；`resume_hitl` L167–211；`polish_prompt` L215–255；`gen` L195–209

<a id="access"></a>
## access

[src/octop/api/common/agent.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/api/common/agent.py) · 79 行

`agent_is_shared` L10–11；`user_owns_agent` L14–15；`assert_agent_owner` L18–23；`_user_may_access` L26–31；`assert_agent_access_row` L34–36；`require_agent_row` L39–61；`require_agent_owner_row` L64–74；`assert_agent_access` L77–79

<a id="limits"></a>
## limits

[src/octop/infra/agents/runtime_limits.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/agents/runtime_limits.py) · 182 行

`_positive_int` L33–44；`agent_recursion_limit` L47–49；`agent_max_input_tokens` L52–54；`_unit_float` L57–72；`_agent_temperature` L75–77；`_agent_top_p` L80–82；`_agent_max_output_tokens` L85–87；`agent_model_settings` L90–102；`resolve_context_max_tokens` L105–110；`agent_runtime_values` L113–115；`merge_agent_runtime_values` L118–132；`apply_agent_runtime_to_stream_request` L135–168

<a id="security"></a>
## security

[src/octop/infra/agents/security/policy_store.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/agents/security/policy_store.py) · 53 行

`_default_policy` L18–23；`SecuritySettingsStore` L26–53；`__init__` L29–30；`load` L32–43；`save` L45–50；`harness_policy` L52–53

<a id="backend"></a>
## backend

[src/octop/infra/backend/resolver.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/backend/resolver.py) · 188 行

`default_agent_backend_spec` L12–31；`windows_neutralize_host_root` L34–65；`_is_host_root` L68–76；`resolve_agent_backend_spec` L79–122；`collect_named_storage_backend_refs` L125–147；`find_agents_using_storage_backend` L150–164；`backend_spec_supports_execution` L167–188

<a id="memory-backend"></a>
## memory-backend

[src/octop/infra/agents/memory_backend.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/agents/memory_backend.py) · 87 行

`memory_backend_from_agent_config` L13–65；`open_memory_kwargs` L68–87

<a id="paths"></a>
## paths

[src/octop/infra/utils/paths.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/utils/paths.py) · 150 行

`PathLayout` L11–150；`from_env` L15–20；`db` L23–24；`logs_dir` L27–29；`log` L32–33；`ensure_logs_dir` L35–39；`ensure_log` L41–44；`config` L47–48；`users_dir` L51–52；`user_dir` L54–55；`agents_dir` L58–60；`expert_market_dir` L63–65；`published_experts_dir` L68–70；`skill_packages_dir` L73–75；`knowledge_dir` L78–80；`agent_workspace` L82–84；`ensure_agent_workspace` L86–90；`ensure_root` L92–94；`plugins_dir` L97–98；`tool_guard_rules_dir` L101–103；`tool_guard_rules_file` L106–107；`backups_dir` L110–112；`ensure_backups_dir` L114–117；`backup_file` L119–121；`ssl_dir` L124–126；`ensure_ssl_dir` L128–131；`connector_cli_dir` L134–136；`connector_cli_instance_dir` L138–145；`ensure_connector_cli_instance_dir` L147–150

<a id="kb-tools"></a>
## kb-tools

[src/octop/infra/knowledge/tools.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/knowledge/tools.py) · 120 行

`_clip_catalog_text` L29–33；`format_search_knowledge_description` L36–53；`_tool_ctx` L56–68；`build_knowledge_tools` L71–120；`search_knowledge` L74–111

<a id="kb-hint"></a>
## kb-hint

[src/octop/infra/knowledge/hint.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/knowledge/hint.py) · 119 行

`catalog_for_selected_bases` L15–40；`_catalog_from_config` L43–58；`_with_enriched_tool_description` L61–91；`KnowledgeSearchHintMiddleware` L94–113；`wrap_model_call` L101–106；`awrap_model_call` L108–113

<a id="kb-jobs"></a>
## kb-jobs

[src/octop/infra/knowledge/jobs.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/knowledge/jobs.py) · 86 行

`reset_index_semaphore_for_tests` L21–24；`_get_index_semaphore` L27–31；`process_document` L34–60；`enqueue_index_document` L63–72；`reindex_all_documents` L75–79；`resume_pending_index_jobs` L82–86；`_run` L68–70

<a id="kb-chunk"></a>
## kb-chunk

[src/octop/infra/knowledge/chunk.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/knowledge/chunk.py) · 21 行

`chunk_text` L6–21

<a id="kb-index"></a>
## kb-index

[src/octop/infra/knowledge/index.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/knowledge/index.py) · 134 行

`Hit` L17–23；`KnowledgeIndex` L26–134；`__init__` L29–31；`path` L34–35；`_connect` L37–38；`_initialize` L40–55；`replace_doc_chunks` L57–92；`delete_doc` L94–96；`search` L98–134

<a id="kb-retrieve"></a>
## kb-retrieve

[src/octop/infra/knowledge/retrieve.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/knowledge/retrieve.py) · 132 行

`retrieve_context` L22–55；`_retrieve_context_sync` L58–101；`_unique_ids` L104–105；`_format_context` L108–132

<a id="kb-params"></a>
## kb-params

[src/octop/infra/knowledge/params.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/knowledge/params.py) · 115 行

`_as_int` L28–38；`_validate_chunk_window` L41–45；`get_advanced_settings` L48–79；`set_advanced_settings` L82–115

<a id="kb-embed"></a>
## kb-embed

[src/octop/infra/knowledge/embed.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/knowledge/embed.py) · 65 行

`embed_knowledge_texts` L16–33；`_embed_remote_batched` L36–65

<a id="connectors"></a>
## connectors

[src/octop/infra/connectors/builder.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/connectors/builder.py) · 620 行

`_mcp_http_headers` L26–27；`normalize_weiyun_mcp_token` L30–41；`normalize_weknora_base_url` L44–53；`mcp_server_name` L56–57；`internal_mcp_url` L60–71；`new_internal_token` L74–75；`build_http_mcp_spec` L78–87；`_build_remote_spec` L90–190；`_build_gateway_spec` L193–209；`validate_create_credentials` L212–424；`_redact_mcp_configs_for_log` L427–449；`_iter_active_connectors` L452–466；`build_mcp_server_configs_for_user` L469–542；`gateway_mcp_server_names` L545–559；`inject_missing_gateway_tools` L562–620

<a id="crypto"></a>
## crypto

[src/octop/infra/connectors/crypto.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/connectors/crypto.py) · 28 行

`_get_fernet` L15–17；`encrypt_credentials` L20–22；`decrypt_credentials` L25–28

<a id="plugins"></a>
## plugins

[src/octop/infra/agents/plugins/manager.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/agents/plugins/manager.py) · 585 行

`normalize_plugin_download_url` L44–58；`_read_global_plugins` L61–77；`_write_global_plugin_enabled` L80–102；`_assert_http_url` L105–111；`_assert_zip_magic` L114–120；`_read_plugin_yaml` L123–125；`parse_plugin_ui_meta` L128–154；`parse_plugin_icon` L157–172；`parse_plugin_requires` L175–183；`PluginManager` L186–585；`__init__` L187–194；`plugins_dir` L197–198；`global_enabled_map` L200–201；`seed_bundled` L203–212；`load_installed` L214–238；`load_missing` L240–273；`list_installed` L275–327；`set_enabled` L329–375；`plugin_dir` L377–382；`resolve_ui_file` L384–417；`install_path` L419–451；`install_archive` L453–490；`install_url` L492–527；`uninstall` L529–535；`plugin_skill_names` L537–548；`sync_skills_to_workspace` L550–585

<a id="quota"></a>
## quota

[src/octop/infra/agents/middleware/token_quota.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/agents/middleware/token_quota.py) · 48 行

`configurable_user_id` L13–23；`TokenQuotaMiddleware` L26–45；`__init__` L29–32；`_enforce` L34–37；`before_agent` L39–41；`abefore_agent` L43–45

<a id="cron"></a>
## cron

[src/octop/infra/cron/manager.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/cron/manager.py) · 310 行

`CronCreateSpec` L31–47；`CronManager` L50–310；`__init__` L53–68；`replace_repos` L70–73；`boot` L75–80；`reload_from_db` L82–98；`shutdown` L100–103；`create` L105–144；`get` L146–147；`list_by_agent` L149–160；`list_all` L162–163；`update` L165–211；`delete` L213–218；`run_now` L220–226；`_make_job` L228–234；`_schedule` L236–257；`_unschedule` L259–261；`_ensure_session` L263–288；`schedule_system_job` L290–300；`unschedule_system_job` L302–306；`has_system_job` L308–310

<a id="delivery"></a>
## delivery

[src/octop/infra/cron/delivery.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/cron/delivery.py) · 314 行

`CronDeliveryCommand` L34–46；`CronDeliveryService` L49–291；`command_from_row` L294–307；`__init__` L52–61；`replace_repos` L63–65；`deliver` L67–87；`_deliver_text` L89–130；`_deliver_agent` L132–170；`_build_agent_request` L172–231；`_attach_turn_knowledge_config` L233–258；`_project_best_effort` L260–274；`_notify_best_effort` L276–291；`_locked` L70–81

<a id="frontend"></a>
## frontend

[dashboard/src/pages/Chat/hooks/chatStore.ts](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/dashboard/src/pages/Chat/hooks/chatStore.ts) · 2253 行

<a id="frontend-package"></a>
## frontend-package

[dashboard/package.json](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/dashboard/package.json) · 86 行

<a id="compose"></a>
## compose

[docker/docker-compose.yml](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/docker/docker-compose.yml) · 55 行

<a id="acp-cli"></a>
## acp-cli

[src/octop/cli/commands/acp.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/cli/commands/acp.py) · 63 行

`_run_acp_server` L11–45；`acp_cmd` L53–63

<a id="acp-settings"></a>
## acp-settings

[src/octop/infra/agents/acp_settings.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/agents/acp_settings.py) · 144 行

`_settings_key` L41–42；`ACPSettingsStore` L45–120；`_runners_response` L123–134；`_parse_config_json` L137–144；`__init__` L48–50；`load_runners` L52–72；`save_runners` L74–77；`_save_raw_runners` L79–82；`_migrate_legacy_from_agents` L84–105；`_strip_legacy_runners` L107–120

<a id="team-doc"></a>
## team-doc

[docs/agent-interop-mailbox.md](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/docs/agent-interop-mailbox.md) · 323 行

<a id="delegation-doc"></a>
## delegation-doc

[docs/agent-delegation.md](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/docs/agent-delegation.md) · 36 行

<a id="db"></a>
## db

[src/octop/infra/db/factory.py](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/src/octop/infra/db/factory.py) · 44 行

`resolve_sqlite_db_path` L12–17；`should_defer_control_plane_db` L20–31；`open_database` L34–44

<a id="license"></a>
## license

[LICENSE](https://github.com/TencentCloud/Octop/blob/757fd12e5dcae7f9303dbfbbf6321a6986694a8b/LICENSE) · 21 行

<a id="h-agent"></a>
## h-agent

**orcakit-harness-agent 1.0.11** · `src/harness_agent/agent.py` · 1923 行

[锁定源码包](https://files.pythonhosted.org/packages/d6/6e/f7f45fc50e4cfc7f2f1e82bf48fe0d8e24cceb207085cede9887bf265087/orcakit_harness_agent-1.0.11.tar.gz) · 包 SHA-256：`4f1c86302fb7bfb25044f7f9c7ed0742a5e80587b436c6a93f3aca9e8acfa175`

`_tool_name_of` L77–86；`HarnessAgent` L89–1853；`_async_close_sqlite_connection` L1856–1861；`_sync_close_sqlite_connection` L1864–1893；`_build_async_sqlite_saver` L1896–1916；`_new_async_saver` L1919–1920；`__init__` L145–202；`config` L209–210；`agent_id` L213–215；`graph` L218–220；`backend` L223–225；`workspace` L228–230；`memory` L233–235；`memory_maintenance_status` L237–242；`checkpointer` L245–251；`protocol` L254–256；`model_factory` L259–266；`is_bootstrapped` L268–275；`append_mcp_tools` L277–287；`replace_mcp_tools` L289–293；`inject_mcp_tools` L295–297；`init_workspace` L299–323；`get_protocol` L325–332；`set_skills_disabled` L334–344；`set_tools_disabled` L346–355；`reload_subagents` L357–359；`list_skill_summaries` L361–369；`list_subagent_summaries` L371–378；`cancel` L382–385；`get_thread_model` L387–388；`set_thread_model` L390–391；`clear_thread_model` L393–394；`_iter_until_cancelled` L396–450；`call` L452–473；`stream` L475–527；`resume_hitl` L529–546；`stream_events` L548–569；`aget_history` L571–647；`aappend_messages` L649–686；`adelete_thread` L688–728；`aget_context_usage` L730–766；`acompact_conversation` L768–812；`_default_max_input_tokens` L814–830；`_read_history_from_graph_state` L832–856；`_read_history_checkpoint` L858–907；`_sync_list_checkpoint_messages` L910–918；`end_session` L922–938；`_invocation` L941–963；`_defer_close_while_busy` L965–976；`close` L978–1001；`aclose` L1003–1018；`__del__` L1020–1022；`__enter__` L1024–1025；`__exit__` L1027–1033；`__aenter__` L1035–1036；`__aexit__` L1038–1044；`_init_paths` L1050–1058；`_resolve_mount_root` L1061–1067；`_peek_backend_mount` L1069–1097；`_host_workspace_path` L1099–1131；`_agent_visible_workspace_dir` L1133–1159；`_host_system_dir` L1161–1164；`_init_logging` L1166–1171；`_init_mcp` L1173–1189；`_init_model_factory` L1191–1221；`_bind_plugin_model_factory` L1223–1232；`_init_graph` L1234–1254；`set_langfuse_callbacks` L1256–1262；`_wrap_graph` L1264–1267；`_sync_protocol_graph` L1269–1278；`_init_protocols` L1280–1282；`_build_backend` L1284–1314；`_wire_workspace_dotenv_for_execute` L1316–1325；`_close_backend` L1327–1332；`_build_tools` L1334–1357；`_ask_user_active` L1359–1367；`_resolve_interrupt_on` L1369–1384；`_build_acp_tools` L1386–1407；`_build_middleware` L1409–1532；`_build_tool_search_middleware` L1534–1552；`_build_bootstrap_middleware` L1554–1566；`_on_bootstrap_complete` L1568–1585；`_resolve_subagents` L1587–1629；`_build_graph` L1631–1732；`_build_seed_model` L1734–1751；`_resolve_checkpointer` L1753–1812；`_release_checkpointer` L1814–1820；`_release_checkpointer_async` L1822–1828；`_prepare_call` L1834–1844；`_get_protocol` L1846–1853；`_call` L464–467；`_stream` L494–509；`_capture_summarization_middleware` L1713–1721

<a id="h-config"></a>
## h-config

**orcakit-harness-agent 1.0.11** · `src/harness_agent/config/__init__.py` · 1112 行

[锁定源码包](https://files.pythonhosted.org/packages/d6/6e/f7f45fc50e4cfc7f2f1e82bf48fe0d8e24cceb207085cede9887bf265087/orcakit_harness_agent-1.0.11.tar.gz) · 包 SHA-256：`4f1c86302fb7bfb25044f7f9c7ed0742a5e80587b436c6a93f3aca9e8acfa175`

`MediaGenerationConfig` L55–136；`ModelConfig` L140–252；`_optional_session_header` L255–259；`ProviderConfig` L263–348；`HarnessAgentConfig` L359–999；`_path_to_str` L1007–1009；`_is_rootfs_path` L1012–1019；`_path_dirs_to_jsonable` L1022–1028；`_skills_dir_to_jsonable` L1031–1037；`_subagents_to_jsonable` L1040–1057；`_subagent_from_dict` L1060–1075；`_acp_runners_to_jsonable` L1078–1079；`_acp_runners_from_jsonable` L1082–1089；`_web_search_tools_to_jsonable` L1092–1100；`__post_init__` L77–98；`to_dict` L100–115；`resolve_api_key` L117–124；`has_api_key` L126–130；`from_dict` L133–136；`__post_init__` L176–188；`is_multimodal` L191–193；`effective_context_window` L196–198；`input_token_budget` L200–207；`to_dict` L213–226；`from_dict` L229–252；`__post_init__` L283–301；`get_model` L303–308；`enabled_models` L310–311；`to_dict` L317–333；`from_dict` L336–348；`__post_init__` L615–682；`resolve_model_ref` L688–702；`pick_default_model_ref` L704–711；`pick_multimodal_model_ref` L713–721；`memory_files` L723–729；`_split_ref` L736–744；`_check_model_ref` L746–750；`to_dict` L770–856；`from_dict` L859–928；`to_file` L930–942；`from_file` L945–955；`from_env` L958–978；`_resolve_config_path` L984–989；`_resolve_config_path_for_load` L992–999

<a id="h-memory"></a>
## h-memory

**orcakit-harness-agent 1.0.11** · `src/harness_agent/memory/runtime.py` · 270 行

[锁定源码包](https://files.pythonhosted.org/packages/d6/6e/f7f45fc50e4cfc7f2f1e82bf48fe0d8e24cceb207085cede9887bf265087/orcakit_harness_agent-1.0.11.tar.gz) · 包 SHA-256：`4f1c86302fb7bfb25044f7f9c7ed0742a5e80587b436c6a93f3aca9e8acfa175`

`MemoryRuntime` L36–267；`__init__` L44–64；`memory` L67–69；`service` L72–74；`middleware` L77–79；`build_tools` L81–85；`build_middleware` L87–161；`end_session` L163–177；`close` L179–202；`__del__` L204–206；`_build_memory` L208–220；`_construct_memory` L222–238；`_memory_backend_config` L240–246；`_build_llm_client` L248–267

<a id="h-memory-mw"></a>
## h-memory-mw

**orcakit-harness-agent 1.0.11** · `src/harness_agent/middleware/memory.py` · 1126 行

[锁定源码包](https://files.pythonhosted.org/packages/d6/6e/f7f45fc50e4cfc7f2f1e82bf48fe0d8e24cceb207085cede9887bf265087/orcakit_harness_agent-1.0.11.tar.gz) · 包 SHA-256：`4f1c86302fb7bfb25044f7f9c7ed0742a5e80587b436c6a93f3aca9e8acfa175`

`_claim_reclaim_slot` L74–91；`_BackgroundExecutor` L94–110；`_bg_pool` L113–118；`MemoryMiddleware` L121–878；`_extract_messages` L886–892；`_get_configurable` L895–934；`_active_model_ref` L937–939；`_find_first` L942–949；`_find_last` L952–959；`_render_record` L962–980；`_stringify_content` L983–998；`_extract_usage` L1001–1021；`_find_turn_trigger_user` L1024–1048；`_filter_visible_messages` L1051–1096；`_split_user_assistant` L1099–1118；`_opt_id` L1121–1123；`submit` L103–110；`name` L157–159；`__init__` L161–253；`before_model` L259–280；`wrap_model_call` L282–288；`awrap_model_call` L290–295；`after_model` L297–360；`abefore_model` L362–363；`aafter_model` L365–366；`end_session` L372–446；`_prepare_recall` L452–478；`_submit_capture` L484–512；`_remember_chat_model` L514–524；`_arm_idle_extract` L530–552；`_on_idle_extract` L554–564；`_cancel_idle_timer` L566–571；`_arm_interval_extract` L577–598；`_on_interval_extract` L600–621；`_stop_interval_timer` L623–630；`shutdown` L632–640；`maintenance_status` L642–645；`_set_status` L647–659；`_maintenance_blocks_io` L661–663；`_arm_maintenance` L669–688；`_on_maintenance` L690–695；`_submit_maintenance` L697–706；`_run_reclaim_pass` L709–756；`_run_maintenance_tick` L758–793；`_stop_maintenance_timer` L795–802；`_write_jsonl` L808–855；`_active_file_path` L857–861；`_maybe_rotate` L863–878；`_runner` L104–108；`_run` L400–441；`_run` L495–510；`_run` L703–704

<a id="h-team"></a>
## h-team

**orcakit-harness-agent 1.0.11** · `src/harness_agent/teams/team_manager.py` · 467 行

[锁定源码包](https://files.pythonhosted.org/packages/d6/6e/f7f45fc50e4cfc7f2f1e82bf48fe0d8e24cceb207085cede9887bf265087/orcakit_harness_agent-1.0.11.tar.gz) · 包 SHA-256：`4f1c86302fb7bfb25044f7f9c7ed0742a5e80587b436c6a93f3aca9e8acfa175`

`TeamManager` L35–464；`__init__` L38–45；`bind_invocation_hooks` L47–55；`bind_peer_enrich` L57–64；`bind_peer_session` L66–81；`set_processor` L87–98；`enabled` L101–103；`inbox` L106–107；`close` L109–111；`aclose` L113–115；`team_tools` L121–129；`list_peers` L135–154；`caller_language` L156–162；`_apply_peer_enrich` L164–176；`_peer_allowlist` L178–190；`_filter_peers` L192–202；`resolve_peer` L204–212；`_match_peer` L215–228；`peer_display_name` L231–232；`_resolve_peer_entry` L234–246；`_call_agent` L252–268；`_invoke_inbox_target` L270–282；`_invoke_peer` L284–324；`_build_peer_request` L326–370；`ask_peer_sync` L372–391；`call_peer` L393–426；`submit_peer` L428–464

<a id="h-inbox"></a>
## h-inbox

**orcakit-harness-agent 1.0.11** · `src/harness_agent/teams/inbox.py` · 289 行

[锁定源码包](https://files.pythonhosted.org/packages/d6/6e/f7f45fc50e4cfc7f2f1e82bf48fe0d8e24cceb207085cede9887bf265087/orcakit_harness_agent-1.0.11.tar.gz) · 包 SHA-256：`4f1c86302fb7bfb25044f7f9c7ed0742a5e80587b436c6a93f3aca9e8acfa175`

`InboxMessage` L34–48；`PeerResult` L52–62；`HarnessAgentInboxManager` L65–281；`__init__` L68–81；`enqueue` L87–113；`get` L115–116；`list` L118–131；`cancel` L133–141；`start` L147–149；`shutdown` L151–159；`cancel_worker` L161–164；`_worker_loop` L170–183；`_is_cancelled` L185–186；`_process` L188–249；`_synthesize_reply` L251–272；`_set_status` L274–276；`_prune_terminal` L278–281

<a id="h-peer"></a>
## h-peer

**orcakit-harness-agent 1.0.11** · `src/harness_agent/middleware/peer.py` · 214 行

[锁定源码包](https://files.pythonhosted.org/packages/d6/6e/f7f45fc50e4cfc7f2f1e82bf48fe0d8e24cceb207085cede9887bf265087/orcakit_harness_agent-1.0.11.tar.gz) · 包 SHA-256：`4f1c86302fb7bfb25044f7f9c7ed0742a5e80587b436c6a93f3aca9e8acfa175`

`has_agent_at_mention` L33–35；`_latest_user_text` L38–43；`_stringify_content` L46–57；`render_peer_prompt` L60–113；`_peer_card_lines` L116–126；`_peer_lines` L129–143；`PeerAgentMiddleware` L146–201；`__init__` L155–159；`wrap_model_call` L161–166；`awrap_model_call` L168–173；`_inject` L175–185；`_prompt_block` L187–201

<a id="h-policy"></a>
## h-policy

**orcakit-harness-agent 1.0.11** · `src/harness_agent/security/models.py` · 356 行

[锁定源码包](https://files.pythonhosted.org/packages/d6/6e/f7f45fc50e4cfc7f2f1e82bf48fe0d8e24cceb207085cede9887bf265087/orcakit_harness_agent-1.0.11.tar.gz) · 包 SHA-256：`4f1c86302fb7bfb25044f7f9c7ed0742a5e80587b436c6a93f3aca9e8acfa175`

`HitlPolicy` L47–52；`FilesystemRule` L56–61；`FilesystemPolicy` L65–69；`PiiPolicy` L73–82；`SkillScanPolicy` L86–89；`ToolGuardPolicy` L93–97；`SecurityPolicy` L101–342；`defaults` L111–128；`to_dict` L130–159；`from_dict` L162–243；`merge` L246–256；`resolve_interrupt_on` L258–305；`resolve_permissions` L307–322；`apply_to_config` L324–342；`_when` L292–301

<a id="h-guard"></a>
## h-guard

**orcakit-harness-agent 1.0.11** · `src/harness_agent/middleware/tool_guard.py` · 122 行

[锁定源码包](https://files.pythonhosted.org/packages/d6/6e/f7f45fc50e4cfc7f2f1e82bf48fe0d8e24cceb207085cede9887bf265087/orcakit_harness_agent-1.0.11.tar.gz) · 包 SHA-256：`4f1c86302fb7bfb25044f7f9c7ed0742a5e80587b436c6a93f3aca9e8acfa175`

`ToolGuardMiddleware` L26–119；`__init__` L29–37；`configure` L39–40；`awrap_tool_call` L42–80；`_await_approval` L82–119

<a id="h-backend"></a>
## h-backend

**orcakit-harness-agent 1.0.11** · `src/harness_agent/backends/__init__.py` · 603 行

[锁定源码包](https://files.pythonhosted.org/packages/d6/6e/f7f45fc50e4cfc7f2f1e82bf48fe0d8e24cceb207085cede9887bf265087/orcakit_harness_agent-1.0.11.tar.gz) · 包 SHA-256：`4f1c86302fb7bfb25044f7f9c7ed0742a5e80587b436c6a93f3aca9e8acfa175`

`resolve_backend` L85–187；`_artifacts_host_target` L195–205；`_artifacts_root_for_workspace` L208–251；`_maybe_wrap_workspace_artifacts` L254–276；`_build_local_shell` L279–329；`_build_filesystem` L332–354；`_build_state` L357–360；`_build_store` L363–373；`_build_composite` L376–415；`spec_supports_execution` L418–444；`_looks_like_backend_instance` L447–449；`_build_s3` L452–473；`_build_postgres` L476–496；`_build_cos` L499–515；`_build_oss` L518–533；`_build_obs` L536–551；`_build_docker` L554–570；`_build_opensandbox` L573–581

<a id="h-acp"></a>
## h-acp

**orcakit-harness-agent 1.0.11** · `src/harness_agent/acp/client.py` · 199 行

[锁定源码包](https://files.pythonhosted.org/packages/d6/6e/f7f45fc50e4cfc7f2f1e82bf48fe0d8e24cceb207085cede9887bf265087/orcakit_harness_agent-1.0.11.tar.gz) · 包 SHA-256：`4f1c86302fb7bfb25044f7f9c7ed0742a5e80587b436c6a93f3aca9e8acfa175`

`ACPHostedClient` L15–199；`__init__` L16–30；`pending_permission` L33–34；`update_cwd` L36–37；`start_prompt` L39–43；`resume_prompt` L45–47；`wait_for_permission_request` L49–50；`resolve_permission` L52–66；`request_permission` L68–102；`session_update` L104–134；`ext_method` L136–138；`ext_notification` L140–142；`_unsupported_method` L144–147；`finish_prompt` L149–152；`_emit_message` L154–157；`_accumulate_assistant_content` L159–162；`_merge_assistant_text` L164–173；`_extract_text_from_content` L175–182；`_tool_event_from_state` L184–199

<a id="h-acp-service"></a>
## h-acp-service

**orcakit-harness-agent 1.0.11** · `src/harness_agent/acp/service.py` · 394 行

[锁定源码包](https://files.pythonhosted.org/packages/d6/6e/f7f45fc50e4cfc7f2f1e82bf48fe0d8e24cceb207085cede9887bf265087/orcakit_harness_agent-1.0.11.tar.gz) · 包 SHA-256：`4f1c86302fb7bfb25044f7f9c7ed0742a5e80587b436c6a93f3aca9e8acfa175`

`_kill_process_tree` L22–35；`_Conversation` L39–49；`ACPService` L52–330；`get_acp_service` L336–337；`init_acp_service` L340–345；`close_acp_service` L348–351；`_schedule_close` L354–370；`_shutdown_services` L373–391；`__init__` L53–56；`run_turn` L58–97；`resume_permission` L99–117；`close_thread_session` L119–123；`close_all_sessions` L125–130；`get_session` L132–134；`get_pending_permission` L136–140；`cancel_turn` L142–159；`_get_runner_config` L161–167；`_get_or_create_session` L169–202；`_find_session_by_acp_id` L204–209；`_open_conversation` L211–258；`_wait_for_prompt_outcome` L260–304；`_close_conversation` L306–319；`_prompt_blocks_to_models` L322–330

<a id="m-service"></a>
## m-service

**harness-memory 0.9.10** · `src/harness_memory/service.py` · 273 行

[锁定源码包](https://files.pythonhosted.org/packages/ab/07/9adef1b44381cc83f91bcb83780d504e2986baefee5a16c967d08b929c92/harness_memory-0.9.10.tar.gz) · 包 SHA-256：`d732ebd81e0fce44b3263f42e967895dec53d1bf7ac0efb10e7477b5920fde84`

`MemoryService` L40–270；`__init__` L54–65；`memory` L68–70；`recall` L76–97；`search` L99–117；`get` L119–128；`save` L134–148；`capture_turn` L150–179；`extract` L181–218；`generate_digest` L224–270

<a id="m-recall"></a>
## m-recall

**harness-memory 0.9.10** · `src/harness_memory/pipeline/recall/__init__.py` · 563 行

[锁定源码包](https://files.pythonhosted.org/packages/ab/07/9adef1b44381cc83f91bcb83780d504e2986baefee5a16c967d08b929c92/harness_memory-0.9.10.tar.gz) · 包 SHA-256：`d732ebd81e0fce44b3263f42e967895dec53d1bf7ac0efb10e7477b5920fde84`

`RecallSnippet` L40–51；`RecallResult` L55–65；`_truncate` L82–85；`_role_for_raw` L88–92；`_role_for_atom` L95–101；`_atom_to_snippet` L104–113；`_raw_to_snippet` L116–123；`recall_multi_source` L126–219；`_render` L222–236；`_multi_token_atoms` L239–257；`_multi_token_raw` L260–274；`recall_for_prompt` L311–372；`_recall_for_prompt_impl` L375–510；`_role_for_layer` L513–520；`_filter_prompt_raw` L523–548；`_session_scope_keys` L551–553；`_raw_from_current_session` L556–563

<a id="m-router"></a>
## m-router

**harness-memory 0.9.10** · `src/harness_memory/pipeline/recall/router.py` · 118 行

[锁定源码包](https://files.pythonhosted.org/packages/ab/07/9adef1b44381cc83f91bcb83780d504e2986baefee5a16c967d08b929c92/harness_memory-0.9.10.tar.gz) · 包 SHA-256：`d732ebd81e0fce44b3263f42e967895dec53d1bf7ac0efb10e7477b5920fde84`

`RoutingDecision` L34–52；`route` L55–115

<a id="m-readme"></a>
## m-readme

**harness-memory 0.9.10** · `README_CN.md` · 264 行

[锁定源码包](https://files.pythonhosted.org/packages/ab/07/9adef1b44381cc83f91bcb83780d504e2986baefee5a16c967d08b929c92/harness_memory-0.9.10.tar.gz) · 包 SHA-256：`d732ebd81e0fce44b3263f42e967895dec53d1bf7ac0efb10e7477b5920fde84`



<a id="g-manager"></a>
## g-manager

**harness-gateway 0.9.8** · `src/harness_gateway/manager.py` · 1023 行

[锁定源码包](https://files.pythonhosted.org/packages/0a/ae/693a178aaf7a4e923a4785e906a34d7606c15192627f0f00184b63f190e8/harness_gateway-0.9.8.tar.gz) · 包 SHA-256：`4ea005ff8e5fd08dc73325dfc3cd63e3086fb41d2c6bf690400b37b84c646b02`

`_config_class_for` L35–62；`ChannelManager` L65–1023；`__init__` L88–121；`set_pre_lock_handler` L123–125；`start` L131–180；`stop` L182–212；`set_constraints` L218–231；`_apply_constraints` L233–238；`enqueue` L244–264；`_put_to_queue` L266–289；`_run_interrupt` L291–303；`push_text` L309–319；`push_content` L321–331；`run_in_session` L333–351；`get_channel` L357–359；`add_channel` L361–513；`_instantiate_channel` L515–552；`_build_config` L554–564；`probe_channel` L566–621；`_register_channel` L623–659；`remove_channel` L661–678；`channel_ids` L681–683；`_worker_loop` L689–739；`_session_lock` L741–744；`_drain_same_session` L746–783；`list_subjects` L789–794；`list_all_users` L796–798；`push_to_all` L800–809；`add_feishu_channel` L815–844；`add_wecom_channel` L846–873；`add_qq_channel` L875–902；`add_dingtalk_channel` L904–931；`add_weixin_channel` L933–960；`add_yuanbao_channel` L962–993；`add_xiaoyi_channel` L995–1003；`add_mqtt_channel` L1005–1013；`add_telegram_channel` L1015–1023

<a id="d-graph"></a>
## d-graph

**deepagents 0.7.9** · `deepagents/graph.py` · 943 行

[锁定源码包](https://files.pythonhosted.org/packages/c4/4b/359aa09b9fb378b9cd10b69cb7bdd75847da03c110939ad01f1db715d0e4/deepagents-0.7.9.tar.gz) · 包 SHA-256：`e62311fe73a752d36b830b2f48352aa63afbd56f47176d924065230d983b248e`

`DeepAgentState` L70–73；`__getattr__` L121–137；`_build_default_model` L140–148；`get_default_model` L163–179；`_merge_fs_interrupt_on` L182–198；`_apply_custom_middleware` L201–235；`create_deep_agent` L268–943

<a id="d-summary"></a>
## d-summary

**deepagents 0.7.9** · `deepagents/middleware/summarization.py` · 2160 行

[锁定源码包](https://files.pythonhosted.org/packages/c4/4b/359aa09b9fb378b9cd10b69cb7bdd75847da03c110939ad01f1db715d0e4/deepagents-0.7.9.tar.gz) · 包 SHA-256：`e62311fe73a752d36b830b2f48352aa63afbd56f47176d924065230d983b248e`

`CompactConversationSchema` L131–132；`SummarizationEvent` L135–145；`TriggerClause` L148–158；`TruncateArgsSettings` L161–188；`SummarizationState` L191–204；`SummarizationDefaults` L207–217；`_token_counter_accepts_tools` L220–252；`compute_summarization_defaults` L255–292；`_is_data_url` L303–312；`_extract_data_url` L315–365；`_decode_data_url` L368–395；`_media_reference_block` L398–416；`_rewrite_data_url_blocks` L419–469；`_upload_response_error` L472–490；`_DeepAgentsSummarizationMiddleware` L493–1619；`create_summarization_middleware` L1629–1703；`create_summarization_tool_middleware` L1706–1793；`SummarizationToolMiddleware` L1796–2160；`name` L504–515；`__init__` L517–618；`model` L622–624；`token_counter` L627–629；`_get_profile_limits` L631–633；`_should_summarize` L635–637；`_determine_cutoff_index` L639–641；`_partition_messages` L643–649；`_create_summary` L651–653；`_acreate_summary` L655–657；`_get_session_id` L659–680；`_get_history_path` L682–693；`_is_summary_message` L695–710；`_filter_summary_messages` L712–725；`_build_new_messages_with_path` L727–758；`_get_effective_messages` L760–774；`_apply_event_to_messages` L777–813；`_compute_state_cutoff` L816–841；`_should_truncate_args` L843–871；`_determine_truncate_cutoff_index` L873–920；`_truncate_tool_call` L922–948；`_count_tokens` L950–988；`_truncate_args` L990–1045；`_offload_inline_media` L1047–1127；`_aoffload_inline_media` L1129–1180；`_offload_to_backend` L1182–1257；`_aoffload_to_backend` L1259–1336；`wrap_model_call` L1338–1477；`awrap_model_call` L1479–1619；`__init__` L1836–1861；`_create_compact_tool` L1863–1894；`_build_compact_result` L1896–1946；`_nothing_to_compact` L1949–1967；`_compact_error` L1970–1994；`_compact_threshold` L1997–1999；`_compact_trigger_clause` L2002–2007；`_is_compaction_clause_met` L2009–2026；`_is_eligible_for_compaction` L2028–2046；`_run_compact` L2048–2080；`_arun_compact` L2082–2114；`wrap_model_call` L2116–2137；`awrap_model_call` L2139–2160；`sync_compact` L1873–1874；`async_compact` L1876–1877
