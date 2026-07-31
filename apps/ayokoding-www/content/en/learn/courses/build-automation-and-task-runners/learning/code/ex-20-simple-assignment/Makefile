# MESSAGE expands NAME immediately, before NAME is changed.
NAME = Ada
MESSAGE := hello $(NAME)
NAME = Grace

.PHONY: show
show:
	@printf '%s\n' "$(MESSAGE)"
