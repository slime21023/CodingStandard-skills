#!/usr/bin/env bash
set -u
shopt -s nullglob

[[ -d skills ]] || { printf '%s\n' 'run from the repository root' >&2; exit 2; }
command -v mq >/dev/null 2>&1 || { printf '%s\n' 'mq not found' >&2; exit 2; }

skills=(go-coding-guidelines rust-coding-guidelines c3-coding-guidelines cpp-coding-guidelines
        develop-readable-typescript python-coding-guidelines kotlin-coding-guidelines
        nim-coding-guidelines testing-principles)
topics=' naming-and-formatting data-and-functions control-flow types null-safety errors modules-and-api abstraction resources-and-memory concurrency unsafe-and-ffi lambdas-and-scope-functions collections-and-idioms testing tooling test-scope test-design test-delivery '
tags=' naming formatting data functions control-flow types null-safety errors result option exceptions modules public-api interfaces generics metaprogramming classes ownership memory resources concurrency async cancellation unsafe ffi lambdas collections testing tooling dependencies build documentation review '
headings=('Summary' 'When to Use' 'Rules' 'Dependencies' 'Tooling' 'Recommended Pattern' 'Pitfalls' 'Testing' 'Checklist' 'Related' 'References')
keys=id,title,summary,language,topic,tags,related,snippets
errors=()
count=0

error() { errors+=("$1: $2"); }

check_topic() {
    local file=$1 language=$2 prefix=$3 dir=${1%/*}
    local name=${file##*/} topic metadata h1 sections blocks path links index_line line heading required
    local key id='' title='' summary='' tag_list='' related_list='' value tag target lang length first_code=''
    local order=-1 i rules=0 checklist=0 rows=0 table_header=0 section='' count_in_index=0
    local -a found=() topic_tags=() related=()
    ((count += 1))
    topic=${name%.md}
    if [[ $topics != *" $topic "* || ( $topic == test-* && $prefix != testing ) || ( $prefix == testing && $topic != test-* ) ]]; then
        error "$file" "unknown topic: $topic"
    fi

    if metadata=$(mq -A 'filter(self, fn(n): is_yaml(n);) | first(self) | frontmatter(self) | [s"keys:" + join(keys(self), ","), s"id:" + get("id"), s"title:" + get("title"), s"summary:" + get("summary"), s"language:" + get("language"), s"topic:" + get("topic"), s"tags:" + join(get("tags"), ","), s"related:" + join(get("related"), ","), s"snippets:" + get("snippets")]' "$file"); then
        while IFS=: read -r key value; do
            case $key in
                keys) [[ $value == "$keys" ]] || error "$file" 'incorrect front matter keys or key order' ;;
                id) id=$value ;;
                title) title=$value ;;
                summary) summary=$value ;;
                language) [[ $value == "$language" ]] || error "$file" "language must be $language" ;;
                topic) [[ $value == "$topic" ]] || error "$file" "topic must be $topic" ;;
                tags) tag_list=$value ;;
                related) related_list=$value ;;
                snippets) [[ $value == unverified ]] || error "$file" 'snippets must be unverified' ;;
            esac
        done <<< "$metadata"
        [[ $metadata == keys:* ]] || error "$file" 'missing front matter'
        [[ $id == "$prefix/$topic" ]] || error "$file" "id must be $prefix/$topic"
        (( ${#summary} >= 1 && ${#summary} <= 200 )) || error "$file" 'summary must contain 1–200 characters'
        IFS=, read -ra topic_tags <<< "$tag_list"
        (( ${#topic_tags[@]} >= 1 && ${#topic_tags[@]} <= 6 )) || error "$file" 'expected 1–6 tags'
        for tag in "${topic_tags[@]}"; do
            [[ -n $tag && $tags == *" $tag "* ]] || error "$file" "unknown tag: $tag"
        done
        IFS=, read -ra related <<< "$related_list"
        for target in "${related[@]}"; do
            if [[ ! $target =~ ^$prefix/[a-z0-9-]+$ || ${target#*/} == index || ! -f $dir/${target#*/}.md ]]; then
                error "$file" "unresolved related topic: $target"
            fi
        done
    else
        error "$file" 'cannot parse front matter; tags and related must be arrays'
    fi

    if h1=$(mq '.h1 | to_text(self)' "$file"); then
        [[ -n $title && $h1 == "$title" ]] || error "$file" 'expected one H1 matching title'
    else
        error "$file" 'cannot read H1'
    fi
    if sections=$(mq '.h2 | to_text(self)' "$file"); then
        while IFS= read -r heading; do
            [[ -n $heading ]] || continue
            for i in "${!headings[@]}"; do
                [[ $heading == "${headings[i]}" ]] && break
            done
            if [[ $heading != "${headings[i]}" ]]; then
                error "$file" "unexpected H2: $heading"
                continue
            fi
            if (( i <= order )); then
                error "$file" "duplicate or out-of-order H2: $heading"
            else
                order=$i
            fi
            found[i]=1
            if [[ $topic == testing && $heading == Testing || $topic == tooling && $heading == Tooling ]]; then
                error "$file" "unexpected H2 for $topic: $heading"
            fi
        done <<< "$sections"
        for required in 0 1 2 5 6 8 10; do
            if [[ $language == any && ( $required == 5 || $required == 10 ) ]]; then continue; fi
            [[ ${found[required]:-0} == 1 ]] || error "$file" "missing H2: ${headings[required]}"
        done
    else
        error "$file" 'cannot read H2 headings'
    fi

    if blocks=$(mq -A 'filter(self, fn(n): is_code(n);) | map(self, fn(n): s"fence:" + attr(n, "lang") + ":" + to_string(len(split(to_text(n), "\n")));)' "$file"); then
        while IFS=: read -r key lang length; do
            [[ $key == fence ]] || continue
            case $lang in
                shell|text|json|toml|yaml|cmake) ;;
                *) [[ $language != any && $lang == "$language" ]] || error "$file" "invalid code block language: ${lang:-<missing>}" ;;
            esac
            (( length <= 40 )) || error "$file" "code block has $length lines (maximum 40)"
        done <<< "$blocks"
    else
        error "$file" 'cannot inspect code blocks'
    fi

    if [[ $topic != tooling && $language != any && ${found[5]:-0} == 1 ]]; then
        if path=$(mq -A 'section::by_title("Recommended Pattern") | first(self) | section::body(self) | filter(self, fn(n): is_code(n);) | first(self) | [s"lang:" + attr(self, "lang"), to_text(self)]' "$file"); then
            IFS= read -r first_code <<< "$path"
            [[ $first_code == "lang:$language" ]] || error "$file" "first Recommended Pattern block must use $language"
            path=${path#*$'\n'}
            path=${path%%$'\n'*}
            if [[ $language == python || $language == nim ]]; then
                [[ $path =~ ^\#\ [^[:space:]] ]] || error "$file" 'first Recommended Pattern block needs a # path comment'
            else
                [[ $path =~ ^//\ [^[:space:]] ]] || error "$file" 'first Recommended Pattern block needs a // path comment'
            fi
        else
            error "$file" 'cannot read first Recommended Pattern block'
        fi
    fi

    if sections=$(mq -A '[section::by_title("Rules"), section::by_title("Pitfalls"), section::by_title("Checklist")]' "$file"); then
        while IFS= read -r line; do
            case $line in
                '## '*) section=${line#'## '} ;;
                '- '*)
                    if [[ $section == Rules ]]; then
                        ((rules += 1))
                        [[ $line =~ ^-\ \*\*(MUST|SHOULD|AVOID|REVIEW\ SIGNAL)\*\*\  ]] || error "$file" 'invalid Rules bullet prefix'
                    elif [[ $section == Checklist ]]; then
                        ((checklist += 1))
                    fi ;;
                '|'*)
                    if [[ $section == Pitfalls ]]; then
                        ((rows += 1))
                        [[ $line =~ ^\|[[:blank:]]*Smell[[:blank:]]*\|[[:blank:]]*Why[[:blank:]]*\|[[:blank:]]*Fix[[:blank:]]*\|$ ]] && table_header=1
                    fi ;;
            esac
        done <<< "$sections"
        (( rules >= 1 )) || error "$file" 'Rules needs at least one bullet'
        (( checklist >= 4 && checklist <= 10 )) || error "$file" 'Checklist needs 4–10 bullets'
        (( table_header && rows >= 5 && rows <= 10 )) || error "$file" 'Pitfalls needs a Smell / Why / Fix table with 3–8 data rows'
    else
        error "$file" 'cannot inspect Rules, Checklist, and Pitfalls'
    fi

    if links=$(mq '.link.url' "$file"); then
        while IFS= read -r target; do
            [[ $target == http://* || $target == https://* ]] && continue
            target=${target%%\#*}
            [[ -z $target || -f $dir/$target ]] || error "$file" "unresolved link: $target"
        done <<< "$links"
    else
        error "$file" 'cannot inspect links'
    fi

    if [[ -f $dir/index.md ]]; then
        index_line="| [$title]($name) | $summary |"
        while IFS= read -r line; do
            [[ $line == "$index_line"* ]] && ((count_in_index += 1))
        done < "$dir/index.md"
        (( count_in_index == 1 )) || error "$file" 'expected exactly one matching title and summary in index.md'
    fi
}

for dir in skills/*/; do
    skill=${dir%/}
    skill=${skill##*/}
    if [[ " ${skills[*]} " != *" $skill "* ]]; then error "$dir" 'unknown skill'; fi
done

for skill in "${skills[@]}"; do
    dir=skills/$skill/references
    index=$dir/index.md
    case $skill in
        develop-readable-typescript) language=typescript; prefix=typescript ;;
        testing-principles) language=any; prefix=testing ;;
        *) language=${skill%-coding-guidelines}; prefix=$language ;;
    esac
    grep -qF 'references/index.md' "skills/$skill/SKILL.md" 2>/dev/null || error "skills/$skill/SKILL.md" 'missing references/index.md link'
    if [[ ! -f $index ]]; then
        error "$index" 'missing catalog'
    elif links=$(mq '.link.url' "$index"); then
        while IFS= read -r target; do
            [[ $target == *.md ]] || continue
            [[ -f $dir/$target ]] || error "$index" "unresolved catalog link: $target"
        done <<< "$links"
    else
        error "$index" 'cannot inspect catalog links'
    fi
    skill_count=$count
    for file in "$dir"/*.md; do
        [[ $file == "$index" ]] || check_topic "$file" "$language" "$prefix"
    done
    (( count > skill_count )) || error "$dir" 'missing topics'
done

if (( ${#errors[@]} )); then
    printf '%s\n' "${errors[@]}" >&2
    exit 1
fi
printf 'OK: %d topic files checked\n' "$count"
